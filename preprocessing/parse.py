import json
from product import Product



def get_data(json_path):

    products_list = []
    with open(json_path, 'r') as f:
        products = json.load(f)
        for product in products:
             # Remove unnecessary fields
            product.pop("variantAsins", None)
            product.pop("variantDetails", None)
            
            img_link = product["highResolutionImages"][0] # take the 1st image only
            # description = product.get("description", "")
            # features = " ".join(product.get("features", []))  # Combine all feature strings
            # text = f"{description} {features}".strip()
            text = product.get("title", "")
            products_list.append(Product(img_link, text, product))

    return products_list


