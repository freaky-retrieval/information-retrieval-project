from PIL import Image
from typing import Dict, List
from PIL import Image


class BaseQuery:
    def __init__(self):
        pass


"Textual query"


class TextQuery(BaseQuery):
    def __init__(self, query: str):
        super(TextQuery, self).__init__()
        self.query = query


"Image query"


class ImageQuery(BaseQuery):
    def __init__(self, query: Image.Image):
        super(ImageQuery, self).__init__()
        self.query = query


"Text + Image query"


class ComplexQuery(BaseQuery):
    def __init__(self, query: str, image: Image.Image):
        super(ComplexQuery, self).__init__()
        self.query = query
        self.image = image


"Image-generative query via description"


class GenerativeQuery(BaseQuery):
    def __init__(self, query: str, samples: int = 3):
        super(GenerativeQuery, self).__init__()
        self.query = query
        self.samples = samples  # number of samples to generate


"Generative Query Response"


class GenerativeQueryResponse:
    def __init__(self, samples: List[str]):
        self.descriptions = samples


"Product data fetched from Milvus by similarity scores. This is the candidate one."


class ProductCandidate:
    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.embedding = data.get("embedding")
        self.metadata = data.get("metadata")
        # TODO: Add more fields as needed


"Product data after filtering and ranking. This is the finalist for UI rendering."


class ProductFinalist:
    def __init__(self, data: Dict):
        assert "score" in data, "Score is required for ranking"

        self.title = data.get("title")
        self.price = data.get("price")
        self.images = data.get("images")
        self.description = data.get("description")
        self.features = data.get("features")
        # TODO: Add more fields as needed


"Top-K response"


class TopKFinalists:
    def __init__(self, finalists: List[ProductFinalist]):
        self.finalists = finalists
        self.k = len(finalists)
        sorted(self.finalists, key=lambda x: x.score, reverse=True)
