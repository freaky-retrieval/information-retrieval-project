from torchmetrics.retrieval import RetrievalMAP
from torchmetrics.retrieval import RetrievalPrecision
from torchmetrics.retrieval import RetrievalRecall
import json
import torch
from validator import Validator

class Evaluator:

    def __init__(self, json_paths, query_path):
        self.json_paths = json_paths
        self.query_path = query_path
        validator = Validator(
            json_paths=json_paths,
            query_path=query_path
        )
        validator.validate()

    def load_data(self):
        with open(self.query_path, 'r') as f:
            queries = json.load(f)
        relevance_scores = []
        relevances = []
        indexes = []
        for idx, query in enumerate(queries):
            scores = [item["relevance_score"] for item in query["retrieved_items"]]
            relevance = [item["is_relevant"] for item in query["retrieved_items"]]
            relevance_scores.extend(scores)
            relevances.extend(relevance)
            indexes.extend([idx] * len(scores))  # Group by query index
        return (
            torch.tensor(relevance_scores, dtype=torch.float),
            torch.tensor(relevances, dtype=torch.int),
            torch.tensor(indexes, dtype=torch.int),
        )

    def recall_at_k(self, at_k=5):
        preds, targets, indexes = self.load_data()
        recall_metric = RetrievalRecall(k=at_k)
        recall = recall_metric(preds=preds, target=targets, indexes=indexes)
        return float(recall)

    def precision_at_k(self, at_k=5):
        preds, targets, indexes = self.load_data()
        precision_metric = RetrievalPrecision(k=at_k)
        precision = precision_metric(preds=preds, target=targets, indexes=indexes)
        return float(precision)

    def map_at_k(self, at_k=5):
        preds, targets, indexes = self.load_data()
        map_metric = RetrievalMAP(k=at_k)
        map_score = map_metric(preds=preds, target=targets, indexes=indexes)
        return float(map_score)

    def f1_at_k(self, beta=1., at_k=5):
        precision = self.precision_at_k(at_k)
        recall = self.recall_at_k(at_k)
        f1 = (1 + beta**2) * (precision * recall) / ((beta**2 * precision) + recall)
        return f1
