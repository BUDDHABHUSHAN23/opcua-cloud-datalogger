# app/beat_scheduler.py

from celery_app import celery
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'monitor-tags-every-5-seconds': {
        'task': 'app.workers.monitor_worker.monitor_tags',
        'schedule': 5.0,  # Every 5 seconds
    },
}
