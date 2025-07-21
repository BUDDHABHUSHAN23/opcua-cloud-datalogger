# backend/app/celery_app.py

import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/0")

celery = Celery("opc_datalogger", broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)

# ✅ Automatically discover tasks in worker modules
celery.autodiscover_tasks([
    "app.workers.monitor_worker", # includes report_worker.py, monitor_worker.py
    "app.workers.report_worker"   # ✅ Add this!
])


# Optional task routing by queue name
celery.conf.update(
    task_routes={
        "app.workers.monitor_worker.*": {"queue": "monitoring"},
        "app.workers.report_worker.*": {"queue": "reporting"},
    }
)

