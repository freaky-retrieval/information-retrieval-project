from pymilvus import MilvusClient

class MilvusLiteConnection:
    _instance = None

    @staticmethod
    def connect(db_path="../../infras/products.db"):
        """
        Singleton connection to Milvus Lite.
        Ensures only one connection is created.
        """
        if MilvusLiteConnection._instance is None:
            MilvusLiteConnection._instance = MilvusClient(db_path)
            print(f"Connected to Milvus Lite at {db_path}")
        return MilvusLiteConnection._instance