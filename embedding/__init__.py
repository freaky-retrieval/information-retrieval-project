from base import BasePipelineModule


class CrawlerData:
    def __init__(self):
        pass

class Data:
    def __init__(self):
        pass

class EmbeddingModule(BasePipelineModule):
    def __init__(self):
        pass

    @classmethod
    def from_env(cls):
        pass

    "Receive data from the crawler"
    def receive(self, data: CrawlerData):
        pass

    "Embed the data"
    def embed(self, data: Data):
        pass