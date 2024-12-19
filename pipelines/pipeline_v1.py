import logging
from PIL import Image

from typing import Optional
from base._dtos import GenerativeQuery
from crawlers import CrawlingModule
from pipelines._base import PipelineBase
from utils.downloaders.image_downloader import ParallelImageFetcher
from embedding import EmbeddingModule
from base import BaseQuery, ComplexQuery, ImageQuery, TextQuery, TopKFinalists
from storages.aws_s3.s3_client import S3StorageClient
from utils.generators._base import Text2ImgGenerativeModule
from utils.generators._flux import FluxHuggingFaceGenerator
from utils.llms._base import LLMModule
from utils.llms._ollama import OllamaLLMModule


class PipelineV1(PipelineBase):
    def __init__(
        self,
        embedding_module: EmbeddingModule,
        s3_storage: S3StorageClient,
        downloader: ParallelImageFetcher,
        crawler: CrawlingModule,
        generator: Optional[Text2ImgGenerativeModule] = None,
        llm: Optional[LLMModule] = None,
    ):
        super(PipelineV1, self).__init__(
            embedding_module, s3_storage, downloader, crawler
        )
        self.generator: Optional[Text2ImgGenerativeModule] = generator
        self.llm: Optional[LLMModule] = llm

    """Serve the query"""

    def serve(self, query: BaseQuery) -> TopKFinalists:
        logging.info("Pipeline V1 is serving the query.")
        return super(PipelineV1, self).serve(query)

    """Serve the query to diffusion model"""

    def generate(self, query: GenerativeQuery) -> Optional[Image.Image]:
        if self.generator is not None:
            description = query.description
            if self.llm is not None:
                response = self.llm.generate(query)
                if response is not None:
                    description = response.descriptions[0]
            logging.info(f"Generating image from diffusion with text: {description}")
            return self.generator.generate(description)
        return None

    @classmethod
    def from_env(cls, with_generator: bool = False, with_llm: bool = False):
        "Load all components from environment variables"
        embedding_module = EmbeddingModule.from_env()
        s3_storage = S3StorageClient.from_env()
        downloader = ParallelImageFetcher.from_env()
        crawler = CrawlingModule.from_env()
        generator = FluxHuggingFaceGenerator.from_env() if with_generator else None
        llm = OllamaLLMModule.from_env() if with_llm else None
        return cls(embedding_module, s3_storage, downloader, crawler, generator, llm)

    def get_name(self):
        return "Pipeline V1"

    def _serve_text(self, query: TextQuery) -> TopKFinalists:
        "Logic to serve text query"
        return TopKFinalists([])

    def _serve_image(self, query: ImageQuery) -> TopKFinalists:
        "Logic to serve image query"
        return TopKFinalists([])

    def _serve_complex(self, query: ComplexQuery) -> TopKFinalists:
        "Logic to serve complex query"
        return TopKFinalists([])


pipeline_v1 = PipelineV1.from_env(with_generator=True, with_llm=True)
