from base import BasePipelineModule
from base import BaseQuery


class EmbeddingModule(BasePipelineModule):
    def __init__(self):
        pass

    @classmethod
    def from_env(cls):
        pass

    # "Receive data from the crawler"
    # def receive(self, data: CrawlerData):
    #     pass

    "Embed the data"
    def embed(self, data: BaseQuery):
        pass