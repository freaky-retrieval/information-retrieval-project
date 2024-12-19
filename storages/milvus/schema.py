from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, utility, Index

def get_collection():
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
        collection = Collection(name=collection_name, schema=schema)
        print(f"Collection '{collection_name}' created.")
        
        # Create index for 'image_embedding'
        collection.create_index(
            field_name="image_embedding",
            index_params={"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
        )
        print("Index created for 'image_embedding' field.")

        # Create index for 'text_embedding'
        collection.create_index(
            field_name="text_embedding",
            index_params={"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
        )
        print("Index created for 'text_embedding' field.")
    else:
        # Load existing collection
        collection = Collection(name=collection_name)
        print(f"Collection '{collection_name}' already exists.")
        
        # Ensure indices for both fields
        index_params = {"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
        existing_indexes = {index.field_name: index for index in collection.indexes}

        # Check and create 'image_embedding' index if missing
        if "image_embedding" not in existing_indexes:
            collection.create_index(field_name="image_embedding", index_params=index_params)
            print("Index created for 'image_embedding' field.")
        else:
            print("Index for 'image_embedding' already exists.")

        # Check and create 'text_embedding' index if missing
        if "text_embedding" not in existing_indexes:
            collection.create_index(field_name="text_embedding", index_params=index_params)
            print("Index created for 'text_embedding' field.")
        else:
            print("Index for 'text_embedding' already exists.")
    
    return collection
