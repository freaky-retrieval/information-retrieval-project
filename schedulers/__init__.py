from celery import Celery
import os


app_name = os.getenv("APP_NAME")
uri = os.getenv("REDIS_URL")

app = Celery(app_name, broker=uri, backend=uri)

# Timezone and periodic task schedule placeholder
app.conf.timezone = "UTC"

HOUR = 3600
DAY = 24 * HOUR

@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(HOUR, crawl_data.s(), name="crawl every hour")
    sender.add_periodic_task(DAY, preprocess_data.s(), name="preprocess every day")


@app.task
def crawl_data():
    "Schedule a task to crawl data from Apify"
    pass


@app.task
def preprocess_data():
    "Schedule a task to crawl data from Apify"
    pass
