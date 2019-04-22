import celery_config
from celery import Celery
import config


def make_celery(app):
    celery = Celery(app.import_name,
                    backend='rpc://',
                    broker=config.CELERY_BROKER_URL,
                    acks_late=False)
    celery.config_from_object(celery_config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery