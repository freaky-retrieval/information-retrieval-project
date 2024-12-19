from pathlib import Path
import sys
sys.path.append(str(Path.cwd()))
# print(sys.path)

from pymilvus import utility, Collection
from storages.milvus.schema import get_collection
from storages.milvus.connection import MilvusConnection

if __name__ == "__main__":
    # Connect to Milvus
    MilvusConnection.connect()
    
    # Collection name
    collection_name = "product_embeddings"
    
    # Check if the collection exists
    if utility.has_collection(collection_name):
        # Drop the collection
        collection = Collection(name=collection_name)
        collection.drop()
        print(f"Collection '{collection_name}' dropped.")
    else:
        print(f"Collection '{collection_name}' does not exist.")
    
    # Recreate the collection
    # collection = get_collection()
    # print(f"Collection '{collection_name}' recreated.")
