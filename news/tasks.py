from celery import shared_task
from django.contrib.auth import get_user_model

from news.models import News
from utils.send_email import Util


@shared_task
def send_news_task(news_id):
    news = News.objects.filter(id=news_id, ready_to_publish=True).first()

    if news:
        users = get_user_model().objects.all()

        for user in users:
            data = {
                "email_body": news.content,
                "to_email": user.email,
                "email_subject": news.title,
            }

            Util.send_email(data)
    else:
        raise Exception("There are no news to be sent")
