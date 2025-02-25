from scheduler.celery import app as celery_app
from scheduler import settings
__all__ = ("celery_app",)

celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)