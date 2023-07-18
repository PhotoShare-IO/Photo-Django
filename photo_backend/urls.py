from django.contrib import admin
from django.urls import path, include

from utils.urls import schema_view as swagger_endpoint

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls"), name="user-endpoints"),
    path("docs/", swagger_endpoint.with_ui("swagger"), name="swagger-docs"),
]
