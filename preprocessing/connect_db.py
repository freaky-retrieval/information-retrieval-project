from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from utils import *

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Define the schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="product_id", dtype=DataType.VARCHAR, max_length=100),  # Unique product identifier
    FieldSchema(name="image_embedding", dtype=DataType.FLOAT_VECTOR, dim=512),
    FieldSchema(name="text_embedding", dtype=DataType.FLOAT_VECTOR, dim=512),
    FieldSchema(name="image_path", dtype=DataType.VARCHAR, max_length=500),
    FieldSchema(name="metadata", dtype=DataType.JSON)
]

schema = CollectionSchema(fields, description="Product embeddings for image-text retrieval")
collection = Collection(name="product_embeddings", schema=schema)



def insert_product_images(collection, product):
    """
    Insert all image embeddings for a product into Milvus.
    
    Args:
        collection: Milvus collection object.
        product: A Product object with img_links, text, and metadata.
    """
    product_id = product.metadata.get("asin")  # Unique product ID
    text_embedding = generate_text_embedding(model, product.text)  # Shared text embedding

    for img_link in product.img_links:
        # Generate image embedding
        image_embedding = generate_image_embedding(model, img_link, transformer)

        # Prepare record
        record = {
            "product_id": product_id,
            "image_embedding": image_embedding,
            "text_embedding": text_embedding,
            "image_path": img_link,
            "metadata": product.metadata  # Full product metadata
        }
        
        # Insert into Milvus
        collection.insert([record])

    print(f"Inserted {len(product.img_links)} images for product: {product_id}")
