from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from celery import shared_task
import celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','interface.settings')

app = Celery('interface')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'request_printers_twice_a_day': {
        'task': 'pages.tasks.request_printers',
        'schedule': crontab(minute='30', hour='8,9,10,11,13,14,15,16,17,19,20,22'),
    }

}
app.conf.timezone = 'Europe/Moscow'