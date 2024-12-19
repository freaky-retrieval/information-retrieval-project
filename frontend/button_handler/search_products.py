# Import image for testing
from frontend.button_handler.product import products

def getProducts(text, listImage):

    return [product for product in products if text in product.title.lower()]