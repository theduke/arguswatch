import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crevo_base.settings")
from django.conf import settings



app = Celery('argus_celery', 
    broker='amqp://localhost', 
    backend="amqp://localhost")

app.conf.update(
    #CELERYBEAT_SCHEDULE = {
    #}
)

from .tasks.checker import ArgusChecker
checker = ArgusChecker()

if __name__ == '__main__':
    app.start()
