from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "Canvas Copilot Backend",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=False,
    include=["app.tasks.grading_tasks"],
)
