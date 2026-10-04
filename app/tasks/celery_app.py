from celery import Celery
from app.core.config import settings


celery_app = Celery(
    "user_service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.email_tasks"],
)