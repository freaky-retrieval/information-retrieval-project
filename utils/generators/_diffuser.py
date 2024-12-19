from utils.generators._base import GenerativeHuggingFaceModuleConfig, GenerativeModule
from PIL import Image


class StableDiffuserV3HuggingFaceGenerator(GenerativeModule):
    MODEL_NAME = "stabilityai/stable-diffusion-3.5-large"

    def __init__(self, config: GenerativeHuggingFaceModuleConfig):
        super(StableDiffuserV3HuggingFaceGenerator, self).__init__(config)


