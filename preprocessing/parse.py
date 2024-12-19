import json
from product import Product
import requests
from pathlib import Path
import torch

import sys
sys.path.append(str(Path('tsbir/code/')))
from clip.model import convert_weights, CLIP
from huggingface_hub import login


def get_data(json_path = 'data/shoes.json'):

    products_list = []
    with open(json_path, 'r') as f:
        products = json.load(f)
        for product in products:
            img_links = product["galleryThumbnails"]
            description = product.get("description", "")
            features = " ".join(product.get("features", []))  # Combine all feature strings
            text = f"{description} {features}".strip()
            products_list.append(Product(img_links, text, product))

    return products_list


def get_model():
    login("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")
    CODE_PATH = Path('tsbir/code/')
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = CLIP.from_pretrained("tcm03/tsbir")
    model = model.to(device)
    return model