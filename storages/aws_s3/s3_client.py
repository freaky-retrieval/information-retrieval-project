from concurrent.futures import ThreadPoolExecutor, as_completed
import io
from typing import List, Optional, Tuple
from boto3 import client
from botocore.client import Config
from PIL import Image
import tenacity
import logging

from storages.aws_s3.config import S3StorageConfig


def _upload_with_retries(client, file_obj: Image.Image, key: str, ext: str, config):
    with io.BytesIO() as output:
        file_obj.save(output, format=ext)
        output.seek(0)
        tenacity.retry(
            wait=tenacity.wait_exponential(multiplier=1, max=10),
            stop=tenacity.stop_after_attempt(config.max_retries),
            retry=tenacity.retry_if_exception_type(Exception),
        )(client.upload_fileobj)(output, config.bucket, key)


def _download_object(s3_client, bucket_name, object_key) -> Optional[Image.Image]:
    """
    Download a specific object and save it to the specified local folder. Updates global progress.
    """
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)

        bytes_stream = io.BytesIO(response["Body"].read())

        image = Image.open(bytes_stream)

        return image
    except Exception as e:
        logging.error(f"Error downloading object {object_key}")
        return None


class S3StorageClient:
    def __init__(self, config: S3StorageConfig):
        self.config = config

        self.client = client(
            "s3",
            endpoint_url=config.endpoint,
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
            region_name=config.region,
            config=Config(signature_version="s3v4"),
        )

        logging.info(f"S3 client initialized with the following config: {config}")

    def upload_file_obj(self, file_obj: Image.Image, key: str):
        ext = file_obj.format
        _upload_with_retries(self.client, file_obj, key, ext, self.config)

    def upload_objs(self, objs: List[Tuple[Image.Image, str]]):
        with ThreadPoolExecutor(max_workers=self.config.num_workers) as executor:
            futures = [
                executor.submit(
                    _upload_with_retries,
                    self.client,
                    obj,
                    key,
                    obj.format,
                    self.config,
                )
                for obj, key in objs
            ]
            for future in as_completed(futures):
                if future.cancelled():
                    logging.warning("Some image upload was cancelled")
                    continue
                future.result()

    def retrieve_objs(self, keys: List[str]) -> List[Image.Image]:
        results = []
        with ThreadPoolExecutor(max_workers=self.config.num_workers) as executor:
            futures = [
                executor.submit(
                    tenacity.retry(
                        wait=tenacity.wait_exponential(multiplier=1, max=10),
                        stop=tenacity.stop_after_attempt(self.config.max_retries),
                        retry=tenacity.retry_if_exception_type(Exception),
                    )(_download_object),
                    self.client,
                    self.config.bucket,
                    key,
                )
                for key in keys
            ]
            for future in as_completed(futures):
                if future.cancelled():
                    logging.warning("Some image download was cancelled")
                    continue
                image = future.result()
                if image is None:
                    logging.warning("Some image download failed")
                    continue
                results.append(image)
        return results
