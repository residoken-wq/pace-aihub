from celery import Celery

from app.core.config import get_settings
from app.core.logging import configure_logging


def create_celery() -> Celery:
    settings = get_settings()
    configure_logging(settings.log_level)
    url = settings.valkey_url.get_secret_value()
    celery = Celery("pace", broker=url, backend=url, include=["worker.tasks"])
    celery.config_from_object("worker.config")
    return celery


app = create_celery()
