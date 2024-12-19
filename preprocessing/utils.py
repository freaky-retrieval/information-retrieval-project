import base64
import requests
from pathlib import Path
from io import BytesIO
from PIL import Image


def encode_image_to_base64(image_path):
    """
    Encode an image to a base64 string.
    Args:
        image_path (str): Path to the image file.
    Returns:
        str: Base64-encoded image string.
    """
    with open(image_path, "rb") as image_file:
        # print("open image successfully")
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_image


def encode_image_url_to_base64(image_url: str) -> str:
    """
    Download an image from a URL and encode it to Base64.
    Args:
        image_url (str): URL of the image.
    Returns:
        str: Base64-encoded image string.
    """
    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to download image from URL: {image_url}. Status code: {response.status_code}"
        )
    image = Image.open(BytesIO(response.content)).convert("RGB")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # Save as JPEG to ensure consistent encoding
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return base64_image


def get_fused_embedding(sketch_path: str | Image.Image, text_query: str) -> list:

    API_URL = "https://rybvz9jrlmmdy0eo.us-east-1.aws.endpoints.huggingface.cloud"
    API_TOKEN = "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"

    # Headers for the API request
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    if type(sketch_path) == str:
        base64_sketch = encode_image_to_base64(sketch_path)
    else:
        with BytesIO() as buffer:
            sketch_path.save(buffer, format="JPEG")
            base64_sketch = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # print(f'base64_sketch: {base64_sketch}')

    # API Payload with 'inputs' key
    payload = {"inputs": {"sketch": base64_sketch, "text": text_query}}

    # Send the API Request
    response = requests.post(API_URL, headers=headers, json=payload)

    # Parse the API Response
    if response.status_code == 200:
        result = response.json()
        if "error" in result:
            print("Error:", result["error"])
            return None
        # print("Fused Embedding:", result["embedding"])
        emb = result["embedding"][0]
        return emb
    else:
        print("Error:", response.status_code, response.text)
        return None


def get_image_embedding(
    image_input: str | Path | Image.Image, is_url: bool = False
) -> list:
    """
    Get image embedding from an Inference Endpoint.
    Args:
        image_input (str | Path): Local image path or image URL.
        is_url (bool): Set to True if the input is an image URL.
    Returns:
        list: Embedding vector for the image.
    """
    API_URL = "https://rybvz9jrlmmdy0eo.us-east-1.aws.endpoints.huggingface.cloud"
    API_TOKEN = "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"

    # Headers for the API request
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # Encode image based on input type
    if is_url:
        base64_image = encode_image_url_to_base64(image_input)
    elif type(image_input) == Path:
        base64_image = encode_image_to_base64(image_input)
    else:
        with BytesIO() as buffer:
            image_input.save(buffer, format="JPEG")
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Prepare payload
    payload = {"inputs": {"image": base64_image}}

    # Send API request
    response = requests.post(API_URL, headers=headers, json=payload)

    # Parse the API response
    if response.status_code == 200:
        result = response.json()
        # print(f'result: {result}')
        if "error" in result:
            print("Error:", result["error"])
            return None
        emb = result["embedding"][0]
        return emb
    else:
        print(f"status code: {response.status_code}")
        print(f"error: {response.text}")
        return None


def get_text_embedding(text: str) -> list:
    """
    Get text embedding from an Inference Endpoint.
    Args:
        text (str): text query
    Returns:
        list: Embedding vector for the text.
    """
    API_URL = "https://rybvz9jrlmmdy0eo.us-east-1.aws.endpoints.huggingface.cloud"
    API_TOKEN = "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"

    # Headers for the API request
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # Prepare payload
    payload = {"inputs": {"text": text}}

    # Send API request
    response = requests.post(API_URL, headers=headers, json=payload)

    # Parse the API response
    if response.status_code == 200:
        result = response.json()
        # print(f'result: {result}')
        if "error" in result:
            print("Error:", result["error"])
            return None
        emb = result["embedding"][0]
        return emb
    else:
        print(f"status code: {response.status_code}")
        print(f"error: {response.text}")
        return None
