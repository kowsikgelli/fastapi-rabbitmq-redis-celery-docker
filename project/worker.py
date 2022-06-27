import os
import zipfile

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://myuser:mypassword@rabbitmq:5672//")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")


@celery.task(name="create_task")
def create_task(filename):
    destination = filename.split(".")[0] + ".zip"
    with zipfile.ZipFile(destination,"w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(filename)
    return True
