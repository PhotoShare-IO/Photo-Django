from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import LoginView, RegistrationView, UserView, ResetPasswordView, ResetPasswordConfirmView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    path("password-reset-confirm/", ResetPasswordConfirmView.as_view(), name="password_reset_confirm"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("user/", UserView.as_view(), name="user"),
]
