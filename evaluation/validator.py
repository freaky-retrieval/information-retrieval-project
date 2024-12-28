import json
import os

class Validator:

    def __init__(self, json_paths, query_path):
        self.json_paths = json_paths
        self.query_path = query_path

    def validate(self):

        num_products = 0
        for json_path in self.json_paths:
            with open(json_path, "r") as f:
                data = json.load(f)
                for product in data:
                    if "asin" not in product or product["asin"] == "" or product["asin"] is None:
                        raise Exception(f"Invalid ASIN in {json_path} with product title {product['title']}")
                    if "summarizedTitle" not in product or product["summarizedTitle"] == "" or product["summarizedTitle"] is None:
                        raise Exception(f"Invalid summarizedTitle in {json_path} with product title {product['title']}")
                    num_products += 1

        query_ids = set()
        with open(self.query_path, "r") as f:
            data = json.load(f)
            for query in data:
                if "query_id" not in query or query["query_id"] == "" or query["query_id"] is None:
                    raise Exception(f"Invalid query_id in {self.query_path} with query {query}")
                if query["query_id"] in query_ids:
                    raise Exception(f"Duplicate query_id in {self.query_path} with query {query}")
                query_ids.add(query["query_id"])
                if "text" not in query or query["text"] == "" or query["text"] is None:
                    raise Exception(f"Invalid text in {self.query_path} with query {query}")
                if "sketch_path" not in query or query["sketch_path"] == "" or query["sketch_path"] is None:
                    raise Exception(f"Invalid sketch_path in {self.query_path} with query {query}")
                if not os.path.exists(query["sketch_path"]):
                    raise Exception(f"Sketch path {query['sketch_path']} does not exist")
                if "retrieved_items" not in query or query["retrieved_items"] == [] or query["retrieved_items"] is None:
                    raise Exception(f"Invalid retrieved_items in {self.query_path} with query {query}")
                retrieved_items = query["retrieved_items"]
                if len(retrieved_items) != num_products:
                    raise Exception(f"Number of retrieved items in query {query['query_id']} does not match number of products in JSON files")
                for item in retrieved_items:
                    if "asin" not in item or item["asin"] == "" or item["asin"] is None:
                        raise Exception(f"Invalid ASIN in retrieved item of query {query['query_id']}")
                    if "relevance_scores" not in item or item["relevance_scores"] == [] or item["relevance_scores"] is None:
                        raise Exception(f"Invalid relevance_scores in retrieved item of query {query['query_id']}")
                    relevance_scores = item["relevance_scores"]
                    if len(relevance_scores) != num_products:
                        raise Exception(f"Number of relevance scores in retrieved item of query {query['query_id']} does not match number of products in JSON files")
                    if "is_relevant" not in item or item["is_relevant"] == [] or item["is_relevant"] is None:
                        raise Exception(f"Invalid is_relevant in retrieved item of query {query['query_id']}")
                    is_relevant = item["is_relevant"]
                    if len(is_relevant) != num_products:
                        raise Exception(f"Number of is_relevant in retrieved item of query {query['query_id']} does not match number of products in JSON files")