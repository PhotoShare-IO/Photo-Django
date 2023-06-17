from django.contrib import admin
from django.urls import path, include

from utils.urls import schema_view as swagger_endpoint

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("docs/", swagger_endpoint.with_ui("swagger"), name="swagger-docs"),
]
