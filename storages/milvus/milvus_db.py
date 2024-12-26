from pymilvus import MilvusClient, DataType
from base import BasePipelineModule
import os

class MilvusDB(BasePipelineModule):
    _instance = None

    @staticmethod
    def connect(db_path):
        """
        Singleton connection to Milvus Lite.
        Ensures only one connection is created.
        """
        if MilvusDB._instance is None:
            MilvusDB._instance = MilvusClient(db_path)
            print(f"Connected to Milvus Lite at {db_path}")
        return MilvusDB._instance

    @classmethod
    def from_env(cls):
        """
        Initialize MilvusDB from environment variables or default configuration.
        Returns:
            An instance of MilvusDB ready to use.
        """
        cur_directory = os.getcwd()
        db_path = os.getenv("MILVUS_DB_PATH", os.path.join(cur_directory, "infras/products.db"))
        cls.connect(db_path)
        return cls

    def add_collection(collection_name="product_embeddings", dimension=512):
        """
        Get or create a Milvus Lite collection and ensure indexes are created.
        """
        if not MilvusDB._instance.has_collection(collection_name):
            # Create the schema
            schema = MilvusDB._instance.create_schema(auto_id=True, enable_dynamic_field=False)
            
            # Add fields to the schema
            schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
            schema.add_field(field_name="product_id", datatype=DataType.VARCHAR, max_length=100)
            schema.add_field(field_name="image_embedding", datatype=DataType.FLOAT_VECTOR, dim=dimension)
            schema.add_field(field_name="text_embedding", datatype=DataType.FLOAT_VECTOR, dim=dimension)
            schema.add_field(field_name="image_path", datatype=DataType.VARCHAR, max_length=500)
            schema.add_field(field_name="metadata", datatype=DataType.JSON)

            # Create the collection
            MilvusDB._instance.create_collection(
                collection_name=collection_name,
                schema=schema
            )
            print(f"Collection '{collection_name}' created.")

            # Prepare index parameters
            index_params = MilvusDB._instance.prepare_index_params()
            
            # Add index for 'image_embedding'
            index_params.add_index(
                field_name="image_embedding",
                index_type="FLAT",  # Updated to use FLAT
                metric_type="IP",  # Inner Product metric
                params={}  # FLAT does not require additional parameters
            )

            # Add index for 'text_embedding'
            index_params.add_index(
                field_name="text_embedding",
                index_type="FLAT",  # Updated to use FLAT
                metric_type="IP",  # Inner Product metric
                params={}  # FLAT does not require additional parameters
            )

            # Create indexes
            MilvusDB._instance.create_index(
                collection_name=collection_name,
                index_params=index_params,
                sync=True  # Ensure synchronous execution
            )
            print(f"Indexes created for collection '{collection_name}'.")
        else:
            print(f"Collection '{collection_name}' already exists.")

            # Ensure indexes exist
            index_params = MilvusDB._instance.prepare_index_params()

            # Check and create 'image_embedding' index if missing
            try:
                MilvusDB._instance.describe_index(collection_name, index_name="image_embedding")
                print("Index for 'image_embedding' already exists.")
            except Exception:
                print("Creating missing 'image_embedding' index...")
                index_params.add_index(
                    field_name="image_embedding",
                    index_type="FLAT",  # Updated to use FLAT
                    metric_type="IP",  # Inner Product metric
                    params={}
                )
                MilvusDB._instance.create_index(
                    collection_name=collection_name,
                    index_params=index_params,
                    sync=True
                )
                print("Index created for 'image_embedding' field.")

            # Check and create 'text_embedding' index if missing
            try:
                MilvusDB._instance.describe_index(collection_name, index_name="text_embedding")
                print("Index for 'text_embedding' already exists.")
            except Exception:
                print("Creating missing 'text_embedding' index...")
                index_params.add_index(
                    field_name="text_embedding",
                    index_type="FLAT",  # Updated to use FLAT
                    metric_type="IP",  # Inner Product metric
                    params={}
                )
                MilvusDB._instance.create_index(
                    collection_name=collection_name,
                    index_params=index_params,
                    sync=True
                )
                print("Index created for 'text_embedding' field.")

        return collection_name






    def insert_records(records, collection_name="product_embeddings"):
        """
        Insert records into the Milvus Lite collection.
        Args:
            collection_name: Name of the collection.
            records: List of records to insert.
        """
        try:
            res = MilvusDB._instance.insert(collection_name=collection_name, data=records)
            print(f"Inserted {len(records)} records.")
            return res
        except Exception as e:
            print(f"Failed to insert records: {str(e)}")

    def search_by_embedding(collection_name="product_embeddings", ts_embedding=None, text_embedding=None, top_k=300):
        """
        Retrieve products from Milvus Lite based on the closest match to an embedding.
        Args:
            collection_name: Name of the collection.
            ts_embedding: Query embedding vector for images (list or numpy array).
            text_embedding: Query embedding vector for text (list or numpy array).
            top_k: Number of nearest neighbors to retrieve.
        Returns:
            List of matching products.
        """
        assert (
            ts_embedding is not None or text_embedding is not None
        ), "At least one of the embeddings must be provided."

        # Define search parameters
        search_params = {"metric_type": "IP", "params": {"nprobe": 10}}

        # Combine results
        alpha = 0.5
        combined_scores = {}

        if ts_embedding:
            # Perform search for image embedding
            ts_results = MilvusDB._instance.search(
                collection_name=collection_name,
                data=[ts_embedding],
                anns_field="image_embedding",
                search_params=search_params,
                limit=top_k,
                output_fields=["product_id", "metadata", "image_path"]
            )
            for result in ts_results:
                combined_scores[result["id"]] = (alpha * result["distance"], result)

        if text_embedding:
            # Perform search for text embedding
            text_results = MilvusDB._instance.search(
                collection_name=collection_name,
                data=[text_embedding],
                anns_field="text_embedding",
                search_params=search_params,
                limit=top_k,
                output_fields=["product_id", "metadata", "image_path"]
            )
            for result in text_results:
                if result["id"] in combined_scores:
                    combined_scores[result["id"]][0] += (1 - alpha) * result["distance"]
                else:
                    combined_scores[result["id"]] = ((1 - alpha) * result["distance"], result)

        # Sort combined results
        sorted_results = sorted(combined_scores.items(), key=lambda x: x[1][0], reverse=True)

        print(f"Found {len(sorted_results)} results.")

        results = []
        unique_product_ids = set()

        for _, obj in sorted_results:
            entity = obj[1]
            if entity.get("product_id") not in unique_product_ids:
                unique_product_ids.add(entity.get("product_id"))
                results.append(entity)

        return results[:30]
