import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/0")

celery = Celery("opc_datalogger", broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)

celery.conf.update(
    task_routes={
        "app.workers.monitor_worker.*": {"queue": "monitoring"},
    }
)
