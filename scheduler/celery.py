


import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler.settings')

app = Celery('scheduler')
app.conf.broker_url = "redis://localhost:6379/0"

# Ensure Celery discovers tasks from all installed Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
