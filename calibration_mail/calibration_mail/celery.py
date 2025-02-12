import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calibration_mail.settings')

app = Celery('calibration_mail')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule the email task
app.conf.beat_schedule = {
    'send-daily-device-report': {
        'task': 'rent_tool_app.tasks.send_daily_device_report',
        'schedule': crontab(hour=18, minute=36),  # Run daily at 8:00
    },
}