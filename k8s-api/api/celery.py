import os
import ssl

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

broker_url = f'rediss://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:6379'
broker_use_ssl = {'ssl_cert_reqs': ssl.CERT_NONE}

app = Celery('api')
app.conf.update(
    broker_url=broker_url,
    broker_use_ssl=broker_use_ssl,
)
app.autodiscover_tasks()
