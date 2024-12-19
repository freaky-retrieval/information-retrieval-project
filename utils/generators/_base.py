import logging
import os
from typing import Optional
from PIL import Image
from huggingface_hub import InferenceClient

from base import BasePipelineModule


class GenerativeHuggingFaceModuleConfig:
    def __init__(self, token: Optional[str] = None):
        self.token = token

    @classmethod
    def from_env(cls):
        return cls(token=os.getenv("HUGGINGFACE_TOKEN"))


class Text2ImgGenerativeModule(BasePipelineModule):
    def __init__(self, config: GenerativeHuggingFaceModuleConfig):
        self.token = config.token
        self.client = InferenceClient(self.MODEL_NAME, token=self.token)

    def generate(
        self,
        query: str,
        width: int = 512,
        height: int = 512,
        inference_steps: int = 20,
        guidance_scale: float = 4.5,
        negative_prompts: str = None,
    ) -> Optional[Image.Image]:
        try:
            image = self.client.text_to_image(
                query,
                negative_prompt=negative_prompts,
                width=width,
                height=height,
                num_inference_steps=inference_steps,
                guidance_scale=guidance_scale,
            )
            return image
        except Exception as e:
            logging.error(f"Request to HuggingFace for image generation failed: {e}")

        return None

    def get_name(self) -> str:
        return self.MODEL_NAME

    @classmethod
    def from_env(cls):
        return cls(GenerativeHuggingFaceModuleConfig.from_env())
