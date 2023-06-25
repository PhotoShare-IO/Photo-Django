from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import LoginView, RegistrationView, UserAPI

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/register/", RegistrationView.as_view(), name="register"),
    path("user/<int:pk>/", UserAPI.as_view(), name="user"),
]
