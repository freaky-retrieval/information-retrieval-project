import base64
from io import BytesIO
import logging
import os
from pathlib import Path
from typing import Dict, List

import requests
import tenacity
from base._core import BasePipelineModule
from preprocessing.product import Product
from PIL import Image


def _encode_image_to_base64(image):
    """
    Download an image from a URL and encode it to Base64.
    Args:
        image_url (str): URL of the image.
    Returns:
        str: Base64-encoded image string.
    """
    response = requests.get(image)
    if response.status_code != 200:
        raise Exception(
            f"Failed to download image from URL: {image}. Status code: {response.status_code}"
        )
    image = Image.open(BytesIO(response.content)).convert("RGB")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # Save as JPEG to ensure consistent encoding
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return base64_image

class PreprocessingConfig:
    def __init__(
        self, url: str, token: str, warmup_timeout: int = 60, retries: int = 3
    ):
        self.url = url
        self.token = token
        self.warmup_timeout = warmup_timeout
        self.retries = retries

    @classmethod
    def from_env(cls):
        return cls(
            url=os.getenv("PREPROCESSING_URL"),
            token=os.getenv("PREPROCESSING_TOKEN"),
            warmup_timeout=int(os.getenv("PREPROCESSING_WARMUP_TIMEOUT", 60)),
            retries=int(os.getenv("PREPROCESSING_RETRIES", 3)),
        )


class PreprocessingPipelineModule(BasePipelineModule):
    def __init__(self, config: PreprocessingConfig):
        super(PreprocessingPipelineModule, self).__init__()
        self.config = config
        self.headers = {"Authorization": f"Bearer {config.token}"}

    def emb_text(self, text: str):
        payload = self._to_text_payload(text)
        return self._retryable__embed_post(payload)

    def embed_image(self, image):
        payload = self._to_image_payload(image)
        return self._retryable__embed_post(payload)

    def transform(self, data: List[Dict]) -> List[Product]:
        products = []
        for item in data:
            item.pop("variantAsins", None)
            item.pop("variantDetails", None)
            img_link = item["highResolutionImages"][0]
            text = item.get("title", "")
            products.append(Product(img_link, text, item))
        return products

    def _retryable__embed_post(self, payload):
        try:
            response = tenacity.retry(
                stop=tenacity.stop_after_attempt(self.config.retries),
                wait=tenacity.wait_exponential(multiplier=1, max=10),
                reraise=False,
            )(
                lambda payload: requests.post(
                    self.config.url, headers=self.headers, json=payload
                )
            )(
                payload
            )
        except Exception as e:
            logging.error(f"Error sending image to preprocessing: {e}")
            return None

        if response.status_code == 200:
            result = response.json()
            if "error" in result:
                logging.error(f"Error: {result['error']}")
                return None
            return result["embedding"][0]

        logging.error(f"Error: {response.status_code}, {response.text}")
        return None

    def _to_image_payload(self, image):
        base64_image = self._encode(image)
        return {"inputs": {"image": base64_image}}

    def _to_text_payload(self, text: str):
        return {"inputs": {"text": text}}

    def _encode(self, image_input) -> str:
        base64_image = _encode_image_to_base64(image_input)
        return base64_image

    @classmethod
    def from_env(cls):
        return cls(PreprocessingConfig.from_env())
