from pathlib import Path
import sys
sys.path.append(str(Path.cwd()))
print(sys.path)

from storages.milvus.connection import MilvusConnection
from storages.milvus.schema import get_collection
from storages.milvus.insert import insert_records
from storages.milvus.query import search_by_embedding
from utils import get_image_embedding
import json
from parse import get_data
import numpy as np


def insert_product_images(collection, product):
    """
    Insert all image embeddings for a product into Milvus.
    
    Args:
        collection: Milvus collection object.
        product: A Product object with img_links, text, and metadata.
    """
    product_id = product.metadata.get("asin", "")  # Unique product ID
    # text_embedding = generate_text_embedding(model, product.text)  # Shared text embedding

    for img_link in product.img_links:
        # Generate image embedding
        image_embedding = get_image_embedding(image_input = img_link, is_url = True)

        # Prepare record
        record = {
            "product_id": product_id,
            "image_embedding": image_embedding,
            "text_embedding": np.zeros(512).tolist(),
            "image_path": img_link,
            "metadata": product.metadata
        }
        
        # Insert into Milvus
        insert_records(collection, [record])

    print(f"Inserted {len(product.img_links)} images for product: {product_id}")


def populate_milvus(json_paths = ['data/shoes.json']):
    """
    Populate Milvus with embeddings for a product.
    
    Args:
        product: A Product object with img_links, text, and metadata.
    """

    MilvusConnection.connect()
    collection = get_collection()

    for json_path in json_paths:

        products_list = get_data(json_path)
        
        for product in products_list:
            insert_product_images(collection, product)
