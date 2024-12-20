from PIL import Image
from typing import Dict, List, Optional
from PIL import Image


class BaseQuery:
    def __init__(self):
        pass


"Textual query"


class TextQuery(BaseQuery):
    def __init__(self, query: str):
        super(TextQuery, self).__init__()
        self.content = query


"Image query"


class ImageQuery(BaseQuery):
    def __init__(self, query: Image.Image):
        super(ImageQuery, self).__init__()
        self.content = query


"Text + Image query"


class ComplexQuery(BaseQuery):
    def __init__(self, query: str, image: Image.Image):
        super(ComplexQuery, self).__init__()
        self.text = query
        self.image = image


"Image-generative query via description"


class GenerativeQuery(BaseQuery):
    def __init__(self, query: str, samples: int = 3):
        super(GenerativeQuery, self).__init__()
        self.description = query
        self.samples = samples  # number of samples to generate


"Generative Query Response"


class GenerativeQueryResponse:
    def __init__(self, samples: List[str]):
        self.descriptions = samples


"Product data after filtering and ranking. This is the finalist for UI rendering."


class ProductFinalist:
    def __init__(self, data: Dict):
        self.title: str = data.get("title")
        self.price: Optional[float] = (
            data.get("price").get("value") if data.get("price") else None
        )
        self.url: str = data.get("url")
        self.rating: float = data.get("stars")
        self.rating_details: Dict[str, float] = data.get("starsBreakdown")
        self.review_count: int = data.get("reviewsCount")
        self.galleryThumbnail: List[str] = data.get("galleryThumbnail")
        self.thumbnailImage: str = data.get("thumbnailImage")
        self.description: str = data.get("description")

"Top-K response"


class TopKFinalists:
    def __init__(self, finalists: List[ProductFinalist]):
        self.state = finalists
        self.k = len(finalists)