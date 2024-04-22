from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"

    def ready(self):
        # This import is important for News model signal that creates celery task.
        # This import will be ignored with flake8, don't delete it.
        import news.signals  # noqa: F401
