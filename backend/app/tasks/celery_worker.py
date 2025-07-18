import os
from celery import Celery
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
    include=[
        "app.workers.monitor_worker",
        # Future: add "app.workers.report_worker", "app.workers.alert_worker"
    ]
)

celery_app.conf.task_routes = {
    "app.workers.monitor_worker.monitor_tags": {"queue": "monitor"},
}

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)