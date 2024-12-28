import logging
from typing import Dict, List
from base._core import BasePipelineModule
from storages.mongo._config import MongoDbConfig
from pymongo import MongoClient, UpdateOne, InsertOne


class MongoDbClient(BasePipelineModule):
    def __init__(self, config: MongoDbConfig):
        self.config = config
        self.client = MongoClient(config.uri)

    def fetch(self, ids: List[str]) -> List[Dict]:
        "Fetch processed data by asins"

        assert len(ids) > 0, "Ids cannot be empty"
        
        return list(self._processed().find({"asin": {"$in": ids}}))

    def pull(self) -> List[Dict]:
        "Pull all unprocessed data"
        return list(self._raw().find({"status": {"$ne": "processed"}}))

    def push(self, data: List[Dict]):
        "Push data to raw collection"
        assert len(data) > 0, "Data cannot be empty"
        assert all("asin" in datum for datum in data), "All data must have asin"

        asins = [datum["asin"] for datum in data]

        existing_asins = set(
            [datum["asin"] for datum in self._raw().find({"asin": {"$in": asins}})]
        )

        data = [datum for datum in data if datum["asin"] not in existing_asins]

        self._raw().bulk_write([InsertOne(datum) for datum in data])

        logging.info(f"Pushed {len(data)} new items to raw collection")

    def process(self, data: List[Dict]):
        "Process data and move to processed collection, mark as processed in raw collection"

        assert len(data) > 0, "Data cannot be empty"
        assert all("asin" in datum for datum in data), "All data must have asin"

        self._raw().bulk_write(
            [
                UpdateOne(
                    {"asin": datum["asin"]},
                    {"$set": {"status": "processed"}},
                    upsert=True,
                )
                for datum in data
            ]
        )
        self._processed().bulk_write([InsertOne(datum) for datum in data])

    def _processed(self):
        return self._at(self.config.collections["processed"])

    def _raw(self):
        return self._at(self.config.collections["raw"])

    def _at(self, collection_name):
        return self.client[self.config.database][collection_name]

    @classmethod
    def from_env(cls):
        return cls(MongoDbConfig.from_env())
