# Import image for testing
import logging
from base import GenerativeQuery
import pipelines

def get_image_from_diffusion(text: str):
    logging.info(f"Generating image from diffusion with text: {text}")
    image = pipelines.instance.generate(GenerativeQuery(text))
    return image
