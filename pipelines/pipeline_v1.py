import logging
from PIL import Image
import tenacity

from typing import Optional
from base._dtos import GenerativeQuery, ProductFinalist
from crawlers import CrawlingModule
from pipelines._base import PipelineBase
from preprocessing.utils import (
    get_fused_embedding,
    get_image_embedding,
    get_text_embedding,
)
from storages.milvus.query import search_by_embedding
from storages.milvus.schema import get_collection
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
        s3_storage: S3StorageClient,
        downloader: ParallelImageFetcher,
        crawler: CrawlingModule,
        generator: Optional[Text2ImgGenerativeModule] = None,
        llm: Optional[LLMModule] = None,
    ):
        super(PipelineV1, self).__init__(s3_storage, downloader, crawler)
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
        s3_storage = S3StorageClient.from_env()
        downloader = ParallelImageFetcher.from_env()
        crawler = CrawlingModule.from_env()
        generator = FluxHuggingFaceGenerator.from_env() if with_generator else None
        llm = OllamaLLMModule.from_env() if with_llm else None
        return cls(s3_storage, downloader, crawler, generator, llm)

    def get_name(self):
        return "Pipeline V1"

    def _serve_text(self, query: TextQuery) -> TopKFinalists:
        # Get embedding
        embedding = tenacity.retry(
            wait=tenacity.wait_fixed(2),
            stop=tenacity.stop_after_delay(10),
            retry=tenacity.retry_if_exception_type(Exception),
        )(get_text_embedding)(query.content)

        # Query Dbs and Post-processing
        candidates = search_by_embedding(get_collection(), None, embedding)

        "Logic to serve text query"
        return TopKFinalists(
            [
                ProductFinalist(candidate[1][1].entity.get("metadata"))
                for candidate in candidates
            ]
        )

    def _serve_image(self, query: ImageQuery) -> TopKFinalists:
        # Get embedding
        embedding = tenacity.retry(
            wait=tenacity.wait_fixed(2),
            stop=tenacity.stop_after_delay(10),
            retry=tenacity.retry_if_exception_type(Exception),
        )(get_image_embedding)(query.content)

        # Query Dbs and Post-processing
        candidates = search_by_embedding(get_collection(), embedding, None)

        "Logic to serve text query"
        return TopKFinalists(
            [
                ProductFinalist(candidate[1][1].entity.get("metadata"))
                for candidate in candidates
            ]
        )

    def _serve_complex(self, query: ComplexQuery) -> TopKFinalists:
        # Get embedding
        embedding = tenacity.retry(
            wait=tenacity.wait_fixed(2),
            stop=tenacity.stop_after_delay(10),
            retry=tenacity.retry_if_exception_type(Exception),
        )(get_fused_embedding)(query.image, query.text)

        # Query Dbs and Post-processing
        candidates = search_by_embedding(get_collection(), embedding, None)

        "Logic to serve text query"
        return TopKFinalists(
            [
                ProductFinalist(candidate[1][1].entity.get("metadata"))
                for candidate in candidates
            ]
        )


instance = PipelineV1.from_env(with_generator=True, with_llm=True)
