import numpy as np
from pymilvus import utility

def search_by_embedding(collection, ts_embedding, text_embedding, top_k=5):
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
    ts_results = collection.search(
        data=[ts_embedding], 
        anns_field="image_embedding",
        param=search_params,
        limit=top_k,
        output_fields=["product_id", "metadata", "image_path"]
    )
    # Search by text embedding against text embeddings
    text_results = collection.search(
        data=[text_embedding],
        anns_field="text_embedding",
        param=search_params,
        limit=top_k,
        output_fields=["product_id", "metadata", "image_path"]
    )

    # Parse results
    # matches = []
    # for hits in query_results:
    #     for hit in hits:
    #         matches.append({
    #             "product_id": hit.entity.get("product_id"),
    #             "metadata": hit.entity.get("metadata"),
    #             "image_path": hit.entity.get("image_path"),
    #             "distance": hit.distance
    #         })

    # Combine results
    alpha = 0.5
    combined_scores = {}
    for result in ts_results[0]:
        combined_scores[result.id] = (alpha * result.distance, result.entity)
    
    for result in text_results[0]:
        if result.id in combined_scores:
            combined_scores[result.id][0] += (1 - alpha) * result.distance
        else:
            combined_scores[result.id] = ((1 - alpha) * result.distance, result.entity)
    
    # Sort combined results
    sorted_results = sorted(combined_scores.items(), key=lambda x: x[1][0], reverse=True)
    
    return sorted_results
