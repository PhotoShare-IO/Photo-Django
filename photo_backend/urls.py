from django.contrib import admin
from django.urls import path, include
from ariadne_django.views import GraphQLView
from photo_backend.schema import schema

from dumb_app.urls import urls as dumb_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(dumb_urls)),
    path('graphql/', GraphQLView.as_view(schema=schema), name='graphql'),
]
