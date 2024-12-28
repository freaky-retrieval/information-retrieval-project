from validator import Validator
import json
import torch
from torcheval.metrics.functional import retrieval_recall
from torcheval.metrics.functional import retrieval_precision

class Evaluator:

    def __init__(self, json_paths, query_path):
        self.json_paths = json_paths
        self.query_path = query_path
        validator = Validator(
            json_paths=json_paths,
            query_path=query_path
        )
        validator.validate()

    def recall_at_k(self, at_k=5):
        queries_recall = []
        with open(self.query_path, 'r') as f:
            queries = json.load(f)
            for query in queries:
                relevance_scores = [item["relevance_score"] for item in query["retrieved_items"]]
                relevances = [item["is_relevant"] for item in query["retrieved_items"]]
                relevance_scores_ts = torch.tensor(relevance_scores, dtype=torch.float)
                relevances_ts = torch.tensor(relevances, dtype=torch.int)
                recall = retrieval_recall(relevance_scores_ts, relevances_ts, k=at_k, value=True)
                queries_recall.append(float(recall))
        # mean recall
        return float(torch.mean(torch.tensor(queries_recall, dtype=torch.float)))
    
    def precision_at_k(self, at_k=5):
        queries_precision = []
        with open(self.query_path, 'r') as f:
            queries = json.load(f)
            for query in queries:
                relevance_scores = [item["relevance_score"] for item in query["retrieved_items"]]
                relevances = [item["is_relevant"] for item in query["retrieved_items"]]
                relevance_scores_ts = torch.tensor(relevance_scores, dtype=torch.float)
                relevances_ts = torch.tensor(relevances, dtype=torch.int)
                precision = retrieval_precision(relevance_scores_ts, relevances_ts, k=at_k, value=True)
                queries_precision.append(float(precision))
        # mean precision
        return float(torch.mean(torch.tensor(queries_precision, dtype=torch.float)))
    
    def f1_at_k(self, beta=1., at_k=5):
        precision = self.precision_at_k(at_k)
        recall = self.recall_at_k(at_k)
        f1 = (1 + beta**2) * (precision * recall) / ((beta**2 * precision) + recall)
        return f1

    

    
    