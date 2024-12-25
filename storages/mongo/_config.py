import dotenv
import os

class MongoDbConfig:
    def __init__(self, uri: str, database: str, **kwargs):
        self.uri = uri
        self.database = database
        self.collections = kwargs.get(
            "collections",
        )

    @classmethod
    def from_env(cls):
        dotenv.load_dotenv()
        return cls(
            uri=os.getenv("MONGO_URI"),
            database=os.getenv("MONGO_COLLECTION"),
            collections={
                "raw": os.getenv("MONGO_RAW_COLLECTION", "raw"),
                "processed": os.getenv("MONGO_PROCESSED_COLLECTION", "processed"),
            },
        )
