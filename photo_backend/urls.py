from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from utils.urls import schema_view as swagger_endpoint

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls"), name="user-endpoints"),
    path("api/", include("posts.urls"), name="posts-endpoints"),
    path("docs/", swagger_endpoint.with_ui("swagger"), name="swagger-docs"),
]

if settings.DEBUG:
    urlpatterns.insert(0, path("__debug__/", include("debug_toolbar.urls")))
