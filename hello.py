import logging

from utils.generators._diffuser import StableDiffuserV3HuggingFaceGenerator
from utils.generators._flux import FluxHuggingFaceGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

logging.info("Starting pipeline")


def main():
    flux = StableDiffuserV3HuggingFaceGenerator.from_env()

    image = flux.generate("A beautiful sunset over the mountains")

    image.save("sunset.jpg")


if __name__ == "__main__":
    main()
