import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'makai.settings')
app = Celery('makai')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
