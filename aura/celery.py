import os
from celery import Celery

# set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')

app = Celery('aura')

# load settings from Django settings, using CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks from installed apps
app.autodiscover_tasks()
