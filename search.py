# @tcm: Outdated

from gc import collect
import os
from pymilvus import MilvusClient
from preprocessing.utils import get_fused_embedding
from milvus_lite_integration import get_collection, search_by_embedding

def main():
    client = MilvusClient("./milvus_demo.db")
    collection_name = get_collection(client, collection_name="product_embeddings", dimension=512)

    # Check if collection is loaded
    if not client.has_collection(collection_name):
        print(f"Collection '{collection_name}' is not loaded. Loading it now...")
        client.load_collection(collection_name)
        print(f"Collection '{collection_name}' has been loaded successfully!")

    # Replace sketch query here
    sketch_path = 'data/sketches/shoes_sketch.jpg'
    text_query = "Sport shoes"
    query_embedding = get_fused_embedding(sketch_path, text_query)

    # Search by embedding
    results = search_by_embedding(client, collection_name, ts_embedding=query_embedding, top_k=10)
    for idx, result in enumerate(results):
        print(f"Result {idx+1}")
        print(f"Product ID: {result['product_id']}")
        print(f"Image path: {result['image_path']}")
        print(f"Distance: {result['distance']}")
        print(f"Asin: {result['metadata']['asin']}")

if __name__ == "__main__":
    main()
