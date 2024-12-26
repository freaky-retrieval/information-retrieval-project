import numpy as np
from pymilvus import utility, MilvusClient


# def search_by_embedding(collection, ts_embedding, text_embedding, top_k=300):
#     """
#     Retrieve products from Milvus based on the closest match to an embedding.
#     Args:
#         collection: Milvus collection object.
#         query_embedding: Query embedding vector (list or numpy array).
#         top_k: Number of nearest neighbors to retrieve.
#     Returns:
#         List of matching products.
#     """
#     assert (
#         ts_embedding is not None or text_embedding is not None
#     ), "At least one of the embeddings must be provided."

#     # Ensure collection is loaded
#     if not utility.has_collection(collection.name):
#         print(f"Loading collection: {collection.name}")

#     collection.load()
#     # Combine results
#     alpha = 0.5
#     combined_scores = {}
#     search_params = {"metric_type": "IP", "params": {"nprobe": 10}}

#     if ts_embedding:
#         # Perform search
#         ts_results = collection.search(
#             data=[ts_embedding],
#             anns_field="image_embedding",
#             param=search_params,
#             limit=top_k,
#             output_fields=["product_id", "metadata", "image_path"],
#         )

#         for result in ts_results[0]:
#             combined_scores[result.id] = (alpha * result.distance, result.entity)

#     if text_embedding:
#         # Search by text embedding against text embeddings
#         text_results = collection.search(
#             data=[text_embedding],
#             anns_field="text_embedding",
#             param=search_params,
#             limit=top_k,
#             output_fields=["product_id", "metadata", "image_path"],
#         )

#         for result in text_results[0]:
#             if result.id in combined_scores:
#                 combined_scores[result.id][0] += (1 - alpha) * result.distance
#             else:
#                 combined_scores[result.id] = (
#                     (1 - alpha) * result.distance,
#                     result.entity,
#                 )

#     # Sort combined results
#     sorted_results = sorted(
#         combined_scores.items(), key=lambda x: x[1][0], reverse=True
#     )

#     print(f"Found {len(sorted_results)} results.")

#     results = []

#     unique_product_ids = set()

#     for hit_id, obj in sorted_results:
#         entity = obj[1].entity
#         if entity.get("product_id") not in unique_product_ids:
#             unique_product_ids.add(entity.get("product_id"))
#             results.append((hit_id, obj))

#     return results[:30]

def search_by_embedding(client, collection_name, ts_embedding=None, text_embedding=None, top_k=300):
    """
    Retrieve products from Milvus Lite based on the closest match to an embedding.
    Args:
        client: Milvus Lite client object.
        collection_name: Name of the collection.
        ts_embedding: Query embedding vector for images (list or numpy array).
        text_embedding: Query embedding vector for text (list or numpy array).
        top_k: Number of nearest neighbors to retrieve.
    Returns:
        List of matching products.
    """
    assert (
        ts_embedding is not None or text_embedding is not None
    ), "At least one of the embeddings must be provided."

    # Define search parameters
    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}

    # Combine results
    alpha = 0.5
    combined_scores = {}

    if ts_embedding:
        # Perform search for image embedding
        ts_results = client.search(
            collection_name=collection_name,
            data=[ts_embedding],
            anns_field="image_embedding",
            search_params=search_params,
            limit=top_k,
            output_fields=["product_id", "metadata", "image_path"]
        )
        for result in ts_results:
            combined_scores[result["id"]] = (alpha * result["distance"], result)

    if text_embedding:
        # Perform search for text embedding
        text_results = client.search(
            collection_name=collection_name,
            data=[text_embedding],
            anns_field="text_embedding",
            search_params=search_params,
            limit=top_k,
            output_fields=["product_id", "metadata", "image_path"]
        )
        for result in text_results:
            if result["id"] in combined_scores:
                combined_scores[result["id"]][0] += (1 - alpha) * result["distance"]
            else:
                combined_scores[result["id"]] = ((1 - alpha) * result["distance"], result)

    # Sort combined results
    sorted_results = sorted(combined_scores.items(), key=lambda x: x[1][0], reverse=True)

    print(f"Found {len(sorted_results)} results.")

    results = []
    unique_product_ids = set()

    for _, obj in sorted_results:
        entity = obj[1]
        if entity.get("product_id") not in unique_product_ids:
            unique_product_ids.add(entity.get("product_id"))
            results.append(entity)

    return results[:30]