from celery import shared_task

from django.contrib.auth import get_user_model
from users.utils import Util
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Create an interval schedule for the periodic task
interval, _ = IntervalSchedule.objects.get_or_create(
    every=30,  # Run the task every 30 sec
    period=IntervalSchedule.SECONDS,
)

# Create a periodic task for sending news updates
PeriodicTask.objects.get_or_create(
    interval=interval,
    name="Send News Updates",
    task="users.tasks.send_news_task",  # Task path
    enabled=True,  # Enable the task
)


@shared_task
def send_news_task():
    users = get_user_model().objects.all()

    for user in users:
        data = {
            "email_body": "Hi, here's today's news!",
            "to_email": user.email,
            "email_subject": "Hi there!",
        }

        Util.send_email(data)

    return None
