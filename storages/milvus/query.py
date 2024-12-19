import numpy as np
from pymilvus import utility

def search_by_embedding(collection, query_embedding, top_k=5):
    """
    Retrieve products from Milvus based on the closest match to an embedding.
    Args:
        collection: Milvus collection object.
        query_embedding: Query embedding vector (list or numpy array).
        top_k: Number of nearest neighbors to retrieve.
    Returns:
        List of matching products.
    """
    # Ensure collection is loaded
    if not utility.has_collection(collection.name):
        print(f"Loading collection: {collection.name}")
        collection.load()
    
    # Perform search
    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
    query_results = collection.search(
        data=[query_embedding], 
        anns_field="image_embedding",
        param=search_params,
        limit=top_k,
        output_fields=["product_id", "metadata", "image_path"]
    )

    # Parse results
    matches = []
    for hits in query_results:
        for hit in hits:
            matches.append({
                "product_id": hit.entity.get("product_id"),
                "metadata": hit.entity.get("metadata"),
                "image_path": hit.entity.get("image_path"),
                "distance": hit.distance
            })
    
    return matches
