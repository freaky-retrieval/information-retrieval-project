from concurrent.futures import ThreadPoolExecutor, as_completed
import io
import os
from typing import List, Optional
import dotenv
from PIL import Image
import requests
from base import BasePipelineModule
import tenacity
import logging


class ImageDownloaderConfig:
    def __init__(self, num_workers: int = 10, timeout: int = 5, max_retries: int = 3):
        self.num_workers = num_workers
        self.timeout = timeout
        self.max_retries = max_retries

    def __repr__(self):
        return (
            f"ImageDownloaderConfig("
            f"num_workers={self.num_workers}, "
            f"timeout={self.timeout}, "
            f"max_retries={self.max_retries})"
        )

    @classmethod
    def from_env(cls):
        dotenv.load_dotenv()

        return cls(
            num_workers=int(os.getenv("IMAGE_DOWNLOADER_NUM_WORKERS", 10)),
            timeout=int(os.getenv("IMAGE_DOWNLOADER_TIMEOUT", 5)),
            max_retries=int(os.getenv("IMAGE_DOWNLOADER_MAX_RETRIES", 3)),
        )


def _download_image(url: str) -> Image.Image:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content))


class ParallelImageFetcher(BasePipelineModule):
    def __init__(self, config: ImageDownloaderConfig):
        self.config = config

        logging.info(f"ImageDownloader initialized with the following config: {config}")

    @classmethod
    def from_env(cls):
        return cls(ImageDownloaderConfig.from_env())

    def download_batches(self, urls: List[str]) -> List[Image.Image]:
        results = []
        with ThreadPoolExecutor(max_workers=self.config.num_workers) as executor:
            futures = [
                executor.submit(
                    tenacity.retry(
                        wait=tenacity.wait_exponential(multiplier=1, max=10),
                        stop=tenacity.stop_after_attempt(self.config.max_retries),
                        retry=tenacity.retry_if_exception_type(
                            requests.RequestException
                        ),
                    )(_download_image),
                    url,
                )
                for url in urls
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

    def download_image(self, url: str) -> Optional[Image.Image]:
        image = tenacity.retry(
            wait=tenacity.wait_exponential(multiplier=1, max=10),
            stop=tenacity.stop_after_attempt(self.config.max_retries),
            retry=tenacity.retry_if_exception_type(requests.RequestException),
        )(_download_image)(url)

        if image is None:
            logging.warning("Image download failed")

        return image
