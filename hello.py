from downloaders.image_downloader import ImageDownloaderModule, ImageDownloaderConfig
from pipelines.pipeline_v1 import PipelineV1
import logging

from storages.aws_s3.config import S3StorageConfig
from storages.aws_s3.s3_client import S3StorageClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

logging.info("Starting pipeline")


def main():
    pass

if __name__ == "__main__":
    main()
