import logging

from crawlers import CrawlingModule
from utils.downloaders.image_downloader import ParallelImageFetcher
from base import BaseQuery, ComplexQuery, ImageQuery, TextQuery, TopKFinalists
from storages.aws_s3.s3_client import S3StorageClient


class PipelineBase:
    def __init__(
        self,
        s3_storage: S3StorageClient,
        downloader: ParallelImageFetcher,
        crawler: CrawlingModule,
    ):
        self.s3_storage: S3StorageClient = s3_storage
        self.downloader: ParallelImageFetcher = downloader
        self.crawler: CrawlingModule = crawler

    def get_name(self):
        return self.__class__.get_name

    """Serve the query"""

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
