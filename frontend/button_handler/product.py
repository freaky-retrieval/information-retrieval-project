from dataclasses import dataclass

@dataclass
class Product:
    title: str            # Product title (e.g., "Echo Dot (4th Gen)")
    url: str              # Product URL (e.g., "https://amazon.com/echo-dot")
    thumbnailImage: str   # URL or path to the product thumbnail image
    price: float          # Price of the product (e.g., 49.99)
    rating: float         # Rating of the product (e.g., 4.5 out of 5)
    galleryThumbnail: list[str]
    description: str
