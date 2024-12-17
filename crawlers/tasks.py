from celery_app import app
from apify_client import ApifyClient
import json
import os
import random

APIFY_API_TOKEN = "apify_api_eSqBk9SYo1IdMGbZDEO6Nceb9VsXex3wXFCl"
client = ApifyClient(APIFY_API_TOKEN)

@app.task
def periodic_task_to_do():
    # Đọc danh sách từ khóa từ file
    keywords_file = "keywords.json"
    with open(keywords_file, "r", encoding="utf-8") as f:
        keywords = json.load(f)

    # Chọn 10 từ khóa ngẫu nhiên
    selected_keywords = random.sample(keywords, 10)
    print(f"Selected keywords: {selected_keywords}")

    results = []

    # Crawl dữ liệu cho mỗi từ khóa
    for keyword in selected_keywords:
        run_input = {
            "categoryUrls": [{"url": f"https://www.amazon.com/s?k={keyword}"}],
            "maxItemsPerStartUrl": 5,  # Crawl tối đa 5 sản phẩm cho mỗi từ khóa
            "useCaptchaSolver": False,
            "scrapeProductVariantPrices": False,
            "scrapeProductDetails": True,
        }

        # Chạy Apify Actor
        print(f"Crawling data for keyword: {keyword}")
        run = client.actor("XVDTQc4a7MDTqSTMJ").call(run_input=run_input)

        # Lấy dữ liệu từ Apify
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)

    # Đọc file JSON hiện tại hoặc tạo mới
    data_file = "data.json"
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Tạo set để tránh trùng lặp
    existing_keys = {json.dumps(item, sort_keys=True) for item in existing_data}
    new_items = [item for item in results if json.dumps(item, sort_keys=True) not in existing_keys]
    print("NEW ITEMS:", new_items)
    # Ghi lại file JSON nếu có dữ liệu mới
    if new_items:
        updated_data = existing_data + new_items
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        print(f"Added {len(new_items)} new items. Data Updated in 'data.json'")
    else:
        print("No new items found. File not updated.")

periodic_task_to_do.delay()