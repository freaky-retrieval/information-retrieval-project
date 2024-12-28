from frontend import app
# from storages.milvus.connection import MilvusConnection
from storages.milvus.milvus_db import MilvusDB

import logging
import os

<<<<<<< HEAD
MilvusDB.connect(
    db_path = os.path.join(os.getcwd(), "infras/products.db")
)
=======

MilvusDB.connect()
>>>>>>> develop-milvus

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    app.run()
