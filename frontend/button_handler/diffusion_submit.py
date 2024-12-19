# Import image for testing
import logging
from base import GenerativeQuery
from pipelines import pipeline_v1


def get_image_from_diffusion(text: str):
    logging.info(f"Generating image from diffusion with text: {text}")
    image = pipeline_v1.generate(GenerativeQuery(text))
    return image
