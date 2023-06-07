from django.urls import path

from .views import DumbView

urls = [path("dumb/", DumbView.as_view())]
