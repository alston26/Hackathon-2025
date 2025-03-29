import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostandfound.settings')

# Create the Celery app
app = Celery('lostandfound')

# Configure using settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps
app.autodiscover_tasks()

# Optional: Add this if you want tasks to access Django ORM
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')