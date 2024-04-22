from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .tasks import send_news_task
from photo_backend.celery import app as celery_app


@receiver(post_save, sender=News)
def send_notification_email(sender, instance, **kwargs):
    if instance.ready_to_publish:
        task = send_news_task.apply_async(
            args=[instance.id], eta=instance.publish_datetime
        )
        instance.celery_task = task.id

        # Don't use instance.save() because it will trigger signal
        News.objects.filter(pk=instance.pk).update(
            celery_task=instance.celery_task
        )
    else:
        if instance.celery_task:
            celery_app.control.revoke(
                str(instance.celery_task), terminate=True
            )
            instance.celery_task = None

            # Don't use instance.save() because it will trigger signal
            News.objects.filter(pk=instance.pk).update(
                celery_task=instance.celery_task
            )

        return None
