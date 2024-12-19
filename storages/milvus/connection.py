from pymilvus import connections

class MilvusConnection:
    _instance = None

    @staticmethod
    def connect(host="localhost", port="19530"):
        """
        Singleton connection to Milvus.
        Ensures only one connection is created.
        """
        if MilvusConnection._instance is None:
            MilvusConnection._instance = connections.connect(
                "default", host=host, port=port
            )
            print(f"Connected to Milvus at {host}:{port}")
        return MilvusConnection._instance