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
            
            img_links = product["galleryThumbnails"]
            description = product.get("description", "")
            features = " ".join(product.get("features", []))  # Combine all feature strings
            text = f"{description} {features}".strip()
            products_list.append(Product(img_links, text, product))

    return products_list


