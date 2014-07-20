import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crevo_base.settings")
from django.conf import settings



app = Celery('argus_celery', 
    broker='amqp://localhost', 
    backend="amqp://localhost")

app.conf.update(
    CELERYBEAT_SCHEDULE = {
    'run-scheduler': {
        'task': 'arguswatch.scheduler',
        'schedule': timedelta(seconds=5),
        'args': [],
    },
})

@app.task
def add(x, y):
    return x + y

from .tasks.checker import ArgusChecker
checker = ArgusChecker()

from .tasks.scheduler import ArgusScheduler
scheduler = ArgusScheduler()


if __name__ == '__main__':
    app.start()
