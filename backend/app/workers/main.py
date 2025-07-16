# backend/app/workers/main.py

from celery import Celery
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

REDIS_BROKER_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "app",
    broker=REDIS_BROKER_URL,
    backend=REDIS_BROKER_URL,
    include=["app.workers.monitor_worker"]  # Import task modules here
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    celery_app.start()
