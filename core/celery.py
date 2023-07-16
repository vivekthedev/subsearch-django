import os
from celery import Celery
from kombu.utils.url import safequote
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "core.settings")

access_key = safequote(settings.AWS_ACCESS_KEY_ID)
secret_key = safequote(settings.AWS_SECRET_ACCESS_KEY)

broker_url = f"sqs://{access_key}:{secret_key}@"
app = Celery("core", broker=broker_url)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
