from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection, Index
from base import BasePipelineModule

class MilvusDB(BasePipelineModule):

    _instance = None
    _collection = None

    @classmethod
    def connect(cls, host="localhost", port="19530"):
        """
        Singleton connection to Milvus.
        Ensures only one connection is created.
        """
        if cls._instance is None:
            cls._instance = connections.connect(
                "default", host=host, port=port
            )
            print(f"Connected to Milvus at {host}:{port}")
        cls.get_collection()
        return cls._instance
    
    @classmethod
    def get_collection(cls):
        """
        Get or create the Milvus collection.
        """
        # Define fields
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="product_id", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="image_embedding", dtype=DataType.FLOAT_VECTOR, dim=512),
            FieldSchema(name="text_embedding", dtype=DataType.FLOAT_VECTOR, dim=512),
            FieldSchema(name="image_path", dtype=DataType.VARCHAR, max_length=500),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]

        # Define schema
        schema = CollectionSchema(fields, description="Product embeddings for image-text retrieval")

        # Check if collection exists using utility.has_collection()
        collection_name = "product_embeddings"
        if not utility.has_collection(collection_name):
            # Create the collection
            cls._collection = Collection(name=collection_name, schema=schema)
            print(f"Collection '{collection_name}' created.")
            
            # Create index for 'image_embedding'
            cls._collection.create_index(
                field_name="image_embedding",
                index_params={"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
            )
            print("Index created for 'image_embedding' field.")

            # Create index for 'text_embedding'
            cls._collection.create_index(
                field_name="text_embedding",
                index_params={"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
            )
            print("Index created for 'text_embedding' field.")
        else:
            # Load existing collection
            cls._collection = Collection(name=collection_name)
            print(f"Collection '{collection_name}' loaded.")
            
            # Ensure indices for both fields
            index_params = {"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
            existing_indexes = {index.field_name: index for index in MilvusDB._collection.indexes}

            # Check and create 'image_embedding' index if missing
            if "image_embedding" not in existing_indexes:
                cls._collection.create_index(field_name="image_embedding", index_params=index_params)
                print("Index created for 'image_embedding' field.")
            else:
                print("Index for 'image_embedding' already exists.")

            # Check and create 'text_embedding' index if missing
            if "text_embedding" not in existing_indexes:
                cls._collection.create_index(field_name="text_embedding", index_params=index_params)
                print("Index created for 'text_embedding' field.")
            else:
                print("Index for 'text_embedding' already exists.")
        
        return cls._collection
    
    @classmethod
    def from_env(cls):
        """
        Initialize MilvusDB from environment variables or default configuration.
        Returns:
            An instance of MilvusDB ready to use.
        """
        cls.connect()
        return cls
    
    @classmethod
    def insert_records(cls, records):
        """
        Insert records into the Milvus collection.
        Args:
            records: List of records to insert.
        """
        try:
            cls._collection.insert(records)
            print(f"Inserted {len(records)} record(s).")
        except Exception as e:
            print(f"Failed to insert records: {str(e)}")

    @classmethod
    def search_by_embedding(cls, ts_embedding, text_embedding, top_k=300):
        """
        Retrieve products from Milvus based on the closest match to an embedding.
        Args:
            collection: Milvus collection object.
            query_embedding: Query embedding vector (list or numpy array).
            top_k: Number of nearest neighbors to retrieve.
        Returns:
            List of matching products.
        """
        assert (
            ts_embedding is not None or text_embedding is not None
        ), "At least one of the embeddings must be provided."

        # Ensure collection existed
        if not utility.has_collection(cls._collection.name):
            print(f"Loading collection: {cls._collection.name}")
            cls._get_collection()

        cls._collection.load()
        # Combine results
        alpha = 0.9375
        combined_scores = {}
        search_params = {"metric_type": "IP", "params": {"nprobe": 10}}

        if ts_embedding:
            # Perform search
            ts_results = cls._collection.search(
                data=[ts_embedding],
                anns_field="image_embedding",
                param=search_params,
                limit=top_k,
                output_fields=["product_id", "metadata", "image_path"],
            )

            for result in ts_results[0]:
                combined_scores[result.id] = [alpha * result.distance, result.entity]

        if text_embedding:
            # Search by text embedding against text embeddings
            text_results = cls._collection.search(
                data=[text_embedding],
                anns_field="text_embedding",
                param=search_params,
                limit=top_k,
                output_fields=["product_id", "metadata", "image_path"],
            )

            for result in text_results[0]:
                if result.id in combined_scores:
                    combined_scores[result.id][0] += (1 - alpha) * result.distance
                else:
                    combined_scores[result.id] = [
                        (1 - alpha) * result.distance,
                        result.entity,
                    ]

        # Sort combined results
        sorted_results = sorted(
            combined_scores.items(), key=lambda x: x[1][0], reverse=True
        )

        print(f"Found {len(sorted_results)} results.")

        results = []

        unique_product_ids = set()

        for hit_id, obj in sorted_results:
            entity = obj[1].entity
            if entity.get("product_id") not in unique_product_ids:
                unique_product_ids.add(entity.get("product_id"))
                results.append((hit_id, obj))

        return results[:30]
