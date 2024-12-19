import os
import json

from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

def extract_data_from_json(json_file):
    """Extract images and text data from a JSON file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract images
    images = data.get("highResolutionImages") or data.get("galleryThumbnails") or []
    
    # Extract texts
    description = data.get("description", "")
    features = " ".join(data.get("features", []))  # Combine all feature strings
    
    # Combine description and features
    text = f"{description} {features}".strip()
    
    return images, text










# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Define the schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="image_embedding", dtype=DataType.FLOAT_VECTOR, dim=512),
    FieldSchema(name="text_embedding", dtype=DataType.FLOAT_VECTOR, dim=512),
    FieldSchema(name="image_path", dtype=DataType.VARCHAR, max_length=500),
]

schema = CollectionSchema(fields, description="Product embeddings for image-text retrieval")
collection = Collection(name="product_embeddings", schema=schema)

# Insert data
def insert_to_milvus(image_embedding, text_embedding, image_path):
    collection.insert([
        {"image_embedding": image_embedding, 
         "text_embedding": text_embedding, 
         "image_path": image_path}
    ])

def query_milvus(sketch, text, model, transformer, nbrs=10):
    """Perform Top-k search for combined sketch and text query."""
    # Generate query embedding
    sketch_embedding = model.encode_sketch(transformer(sketch).unsqueeze(0).cuda())
    text_embedding = model.encode_text(tokenize([text]).cuda())
    sketch_embedding /= sketch_embedding.norm(dim=-1, keepdim=True)
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)
    query_embedding = model.feature_fuse(sketch_embedding, text_embedding).cpu().numpy()

    # Search Milvus
    collection.load()
    results = collection.search(
        data=[query_embedding],
        anns_field="image_embedding",  # Search on image embeddings
        param={"metric_type": "COSINE", "params": {"nprobe": 10}},
        limit=nbrs,
        output_fields=["image_path"]
    )
    return results
