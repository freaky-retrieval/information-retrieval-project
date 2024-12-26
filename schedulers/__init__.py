from celery import Celery
import os

# Initialize Celery
uri = "redis://{host}:{port}/{db}".format(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=os.getenv("REDIS_PORT", 6379),
    db=os.getenv("REDIS_DB", 0),
)

app_name = os.getenv("CELERY_APP_NAME", "tasks")

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
