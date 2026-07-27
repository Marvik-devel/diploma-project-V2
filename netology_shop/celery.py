import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netology_shop.settings')

app = Celery('netology_shop')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим tasks
app.autodiscover_tasks()