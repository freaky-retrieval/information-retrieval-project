from utils.generators._base import GenerativeHuggingFaceModuleConfig, Text2ImgGenerativeModule
from PIL import Image


class FluxHuggingFaceGenerator(Text2ImgGenerativeModule):
    MODEL_NAME = "black-forest-labs/FLUX.1-dev"

    def __init__(self, config: GenerativeHuggingFaceModuleConfig):
        super(FluxHuggingFaceGenerator, self).__init__(config)
