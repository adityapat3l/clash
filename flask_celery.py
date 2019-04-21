import celery_config
from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name,
                    backend='rpc://',
                    broker='amqp://qkimbptm:ReMXxlAqYv6i-qde34kBSBsk9weou1eG@reindeer.rmq.cloudamqp.com/qkimbptm',
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