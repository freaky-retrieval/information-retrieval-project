from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import random
from typing import Dict, List
from celery import Celery
import os
from apify_client import ApifyClient
from copy import deepcopy
from preprocessing import PreprocessingConfig, PreprocessingPipelineModule
from storages.milvus.milvus_db import MilvusDB
from storages.mongo import MongoDbClient
from storages.mongo._config import MongoDbConfig

# CELEERY
app_name = os.getenv("APP_NAME")
redis_uri = os.getenv("REDIS_URL")
# APIFY
apify_api_token = os.getenv("APIFY_API_TOKEN")
keywords = os.getenv("KEYWORDS").split(",")
actor_id = os.getenv("APIFY_ACTOR_ID")
# MONGO
mongo_config = MongoDbConfig.from_env()
# PREPROCESSING
preprocessing_config = PreprocessingConfig.from_env()

app = Celery(app_name, broker=redis_uri, backend=redis_uri)

# Timezone and periodic task schedule placeholder
app.conf.timezone = "UTC"

# Constants
MINUTE = 60
HOUR = 3600
DAY = 24 * HOUR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(10, crawl_data.s(), name="crawl every hour")
    sender.add_periodic_task(
        20, preprocess_data.s(), name="preprocess every day"
    )


def _per_thread_crawling(keyword: str, apify_client: ApifyClient) -> List[Dict]:
    "Crawl data for a single keyword"
    run_input = {
        "categoryUrls": [{"url": f"https://www.amazon.com/s?k={keyword}"}],
        "maxItemsPerStartUrl": 50,  # Crawl tối đa 5 sản phẩm cho mỗi từ khóa
        "useCaptchaSolver": False,
        "scrapeProductVariantPrices": False,
        "scrapeProductDetails": True,
    }
    logging.info(f"Crawling data for keyword: {keyword}")
    run = apify_client.actor(actor_id).call(run_input=run_input)
    results = []
    for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)
    return results


@app.task
def crawl_data():
    "Schedule a task to crawl data from Apify"
    apify_client = ApifyClient(apify_api_token)
    mongo_client = MongoDbClient(mongo_config)

    print(f"Keywords: {keywords}")

    selected_keywords = random.sample(keywords, 20)
    logging.info(f"Selected keywords: {selected_keywords}")
    results = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(_per_thread_crawling, keyword, apify_client)
            for keyword in selected_keywords
        ]
        for future in as_completed(futures):
            results.extend(future.result())

    mongo_client.push(results)
    logging.info("Crawling task completed.")


@app.task
def preprocess_data():
    "Schedule a task to process data from Apify"
    logging.info("Preprocessing data")

    print("Preprocessing data")

    mongo_client = MongoDbClient(mongo_config)
    preprocessing_client = PreprocessingPipelineModule(preprocessing_config)

    data = mongo_client.pull()
    if len(data) == 0:
        logging.info("No new data to process")
        return

    logging.info(f"Processing {len(data)} items")

    cloned_data = deepcopy(data)
    transformed_data = preprocessing_client.transform(cloned_data)
    records = []

    for product in transformed_data:
        product_id = product.metadata.get("asin", "")
        text_embedding = preprocessing_client.emb_text(product.text)
        img_link = product.img_link

        # Generate image embedding
        image_embedding = preprocessing_client.embed_image(img_link)

        # Prepare record
        record = {
            "product_id": product_id,
            "image_embedding": image_embedding,
            "text_embedding": text_embedding,
            "image_path": img_link,
            "metadata": product.metadata,
        }

        records.append(record)

    # Insert into Milvus
    MilvusDB.insert_records([record])
    logging.info("Inserted records into Milvus")

    # Move records to processed collection
    mongo_client.process(data)
    logging.info("Preprocessing task completed.")
