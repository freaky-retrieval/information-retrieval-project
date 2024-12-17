import logging
from crawlers import CrawlingModule
from downloaders.image_downloader import ImageDownloaderModule
from embedding import EmbeddingModule
from base import BaseQuery, ComplexQuery, ImageQuery, TextQuery, TopKFinalists
from storages.aws_s3.s3_client import S3StorageClient


class PipelineBase:
    def __init__(
        self,
        embedding_module: EmbeddingModule,
        s3_storage: S3StorageClient,
        downloader: ImageDownloaderModule,
        crawler: CrawlingModule,
    ):
        self.embedding_module: EmbeddingModule = embedding_module
        self.s3_storage: S3StorageClient = s3_storage
        self.downloader: ImageDownloaderModule = downloader
        self.crawler: CrawlingModule = crawler

    def get_name(self):
        return self.__class__.get_name

    def serve(self, query: BaseQuery) -> TopKFinalists:
        if type(query) == TextQuery:
            logging.info(f"{self.get_name()} is serving a text query.")
            return self._serve_text(query)
        elif type(query) == ImageQuery:
            logging.info(f"{self.get_name()} is serving an image query.")
            return self._serve_image(query)
        elif type(query) == ComplexQuery:
            logging.info(f"{self.get_name()} is serving a complex query.")
            return self._serve_complex(query)

    def _serve_text(self, query: TextQuery) -> TopKFinalists:
        raise NotImplementedError

    def _serve_image(self, query: ImageQuery) -> TopKFinalists:
        raise NotImplementedError

    def _serve_complex(self, query: ComplexQuery) -> TopKFinalists:
        raise NotImplementedError

class PipelineV1(PipelineBase):
    def __init__(
        self,
        embedding_module: EmbeddingModule,
        s3_storage: S3StorageClient,
        downloader: ImageDownloaderModule,
        crawler: CrawlingModule,
    ):
        super(PipelineV1, self).__init__(
            embedding_module, s3_storage, downloader, crawler
        )

    @classmethod
    def from_env(cls):
        "Load all components from environment variables"
        embedding_module = EmbeddingModule.from_env()
        s3_storage = S3StorageClient.from_env()
        downloader = ImageDownloaderModule.from_env()
        crawler = CrawlingModule.from_env()
        return cls(embedding_module, s3_storage, downloader, crawler)

    def get_name(self):
        return "Pipeline V1"

    def serve(self):
        logging.info("Pipeline V1 is serving the query.")
        super(PipelineV1, self).serve()

    def _serve_text(self, query: TextQuery) -> TopKFinalists:
        "Logic to serve text query"
        return TopKFinalists([])

    def _serve_image(self, query: ImageQuery) -> TopKFinalists:
        "Logic to serve image query"
        return TopKFinalists([])

    def _serve_complex(self, query: ComplexQuery) -> TopKFinalists:
        "Logic to serve complex query"
        return TopKFinalists([])
