from celery import Celery

# Initialize Celery
app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Timezone and periodic task schedule placeholder
app.conf.timezone = "UTC"
app.conf.beat_schedule = {
    'add-every-minute': {
        'task': 'tasks.periodic_task_to_do',
        'schedule': 10.0,   # This runs the task every minute
    },
}