from typing import List
from PIL import Image
from frontend.button_handler.product import products

def get_products(text, images: List[Image.Image]):

    return [product for product in products if text in product.title.lower()]