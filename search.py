from gc import collect
import os
from storages.milvus.connection import MilvusConnection
from storages.milvus.query import search_by_embedding
from storages.milvus.schema import get_collection
from preprocessing.utils import get_fused_embedding, get_text_embedding
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
    ts_embedding = get_fused_embedding(sketch_path, text_query)
    text_embedding = get_text_embedding(text_query)

    results = search_by_embedding(collection, ts_embedding, text_embedding)
    for idx, (hit_id, result) in enumerate(results):
        print(f"Result {idx+1}")
        # result[0]: float
        # result[1]: pymilvus.client.abstract.Hit
        entity = result[1].entity
        print(f"Product ID: {entity.get('product_id')}")
        print(f"Image path: {entity.get('image_path')}")
        print(f"Distance: {entity.get('distance')}")
        print(f"Asin: {entity.get('metadata')['asin']}")