from base import BasePipelineModule
import dotenv

dotenv.load_dotenv(dotenv_path="crawler/.env")

class CrawlingModule(BasePipelineModule):
    def __init__(self):
        pass

    @classmethod
    def from_env(cls):
        return cls()
