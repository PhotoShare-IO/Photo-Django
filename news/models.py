from django_ckeditor_5.fields import CKEditor5Field
from django.db import models


class News(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    content = CKEditor5Field(verbose_name="Content", config_name="extends")
    publish_datetime = models.DateTimeField(verbose_name="Publish date")
    ready_to_publish = models.BooleanField(
        verbose_name="Ready to publish", default=False
    )
    celery_task = models.UUIDField(
        verbose_name="Celery task", editable=False, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.title}, {self.publish_datetime}"
