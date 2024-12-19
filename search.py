from gc import collect
import os
from storages.milvus.connection import MilvusConnection
from storages.milvus.query import search_by_embedding
from storages.milvus.schema import get_collection
from preprocessing.utils import get_fused_embedding
from pymilvus import utility

if __name__ == "__main__":
    MilvusConnection.connect()
    collection = get_collection()
    load_state = utility.load_state(collection.name)
    if load_state != "Loaded":
        print(f"Collection '{collection.name}' is not loaded. Loading it now...")
        collection.load()
        print(f"Collection '{collection.name}' has been loaded successfully!")

    # replace sketch query here
    sketch_path = 'data/sketches/shoes_sketch.jpg'
    text_query = "Sport shoes"
    query_embedding = get_fused_embedding(sketch_path, text_query)

    results = search_by_embedding(collection, query_embedding)
    for idx, result in enumerate(results):
        print(f"Result {idx+1}")
        print(f"Product ID: {result['product_id']}")
        print(f"Image path: {result['image_path']}")
        print(f"Distance: {result['distance']}")
        print(f"Asin: {result['metadata']['asin']}")