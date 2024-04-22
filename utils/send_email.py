import logging
import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.email.send()
        except Exception as e:
            logging.exception(e)


class Util:
    @staticmethod
    def send_email(data):
        plain_body = strip_tags(data["email_body"])

        html_message = render_to_string(
            "news/email_template.html",
            {"subject": data["email_subject"], "message": plain_body},
        )
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=data["email_subject"],
            body=plain_message,
            to=[data["to_email"]],
        )
        email.attach_alternative(html_message, "text/html")
        EmailThread(email).start()
