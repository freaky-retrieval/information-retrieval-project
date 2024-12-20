from typing import List, Optional
from PIL import Image
from base import ComplexQuery, ImageQuery, TextQuery
from base import ProductFinalist
from pipelines import pipeline_v1
from frontend.button_handler.product import Product as UIProduct

# def is_clean_data(data) -> bool:
#     try:
#         # Ensure the data can be encoded and decoded in UTF-8
#         encoded_data = data.encode('utf-8')
#         decoded_data = encoded_data.decode('utf-8')

#         # Check if the data is alphanumeric
#         return decoded_data.isalnum()
#     except UnicodeDecodeError:
#         return False

# def data_cleaner(data):
#     if is_clean_data(data):
#         return data
#     else:
#         return None

def _map_to_ui_product(product: ProductFinalist) -> UIProduct:
    return UIProduct(
        title=product.title,
        url=product.url,
        price=product.price,
        rating=product.rating,
        galleryThumbnail=product.galleryThumbnail,
        thumbnailImage=product.thumbnailImage,
        description=product.description
    )




def get_products(text: Optional[str], image: Optional[Image.Image]) -> List[UIProduct]:
    if text and image:
        query = ComplexQuery(text, image)
    elif text:
        query = TextQuery(text)
    elif image:
        query = ImageQuery(image)
    else:
        return []

    finalists = pipeline_v1.instance.serve(query)

    if not finalists:
        return []

    return list(map(_map_to_ui_product, finalists.state))
