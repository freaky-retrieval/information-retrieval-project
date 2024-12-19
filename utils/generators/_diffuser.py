from utils.generators._base import GenerativeHuggingFaceModuleConfig, Text2ImgGenerativeModule
from PIL import Image


class StableDiffuserV3HuggingFaceGenerator(Text2ImgGenerativeModule):
    MODEL_NAME = "stabilityai/stable-diffusion-3.5-large"

    def __init__(self, config: GenerativeHuggingFaceModuleConfig):
        super(StableDiffuserV3HuggingFaceGenerator, self).__init__(config)


