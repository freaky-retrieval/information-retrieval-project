import os
from typing import Optional

import dotenv


class S3StorageConfig:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        num_workers: int = 10,
        timeout: int = 5,
        max_retries: int = 3,
        region: Optional[str] = None,
    ):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.region = region

        self.num_workers = num_workers
        self.timeout = timeout
        self.max_retries = max_retries

    def __repr__(self):
        return (
            f"S3StorageConfig("
            f"endpoint={self.endpoint}, "
            f"access_key={self.access_key}, "
            f"secret_key={self.secret_key}, "
            f"bucket={self.bucket}, "
            f"region={self.region}, "
            f"num_workers={self.num_workers}, "
            f"timeout={self.timeout}, "
            f"max_retries={self.max_retries})"
        )

    @classmethod
    def from_env(cls):
        dotenv.load_dotenv()
        return cls(
            endpoint=os.getenv("S3_ENDPOINT"),
            access_key=os.getenv("S3_ACCESS_KEY"),
            secret_key=os.getenv("S3_SECRET_KEY"),
            bucket=os.getenv("S3_BUCKET"),
            region=os.getenv("S3_REGION"),
            num_workers=int(os.getenv("S3_NUM_WORKERS", 10)),
            timeout=int(os.getenv("S3_TIMEOUT", 5)),
            max_retries=int(os.getenv("S3_MAX_RETRIES", 3)),
        )
