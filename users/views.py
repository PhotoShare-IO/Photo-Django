from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import views, serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import (
    UserSerializer,
    UserLoginDataSerializer,
    UserLoginSerializer,
    UserPasswordResetSerializer,
    UserPasswordResetConfirmSerializer,
)
from .swagger import register_schema, login_schema
from .utils import Util


class RegistrationView(views.APIView):
    @swagger_auto_schema(
        tags=["auth"],
        responses={200: UserLoginDataSerializer()},
        request_body=register_schema,
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = RefreshToken.for_user(user)
        return Response(
            UserLoginDataSerializer(
                {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "tokens": {
                        "access": str(tokens.access_token),
                        "refresh": str(tokens),
                    },
                }
            ).data
        )


class LoginView(views.APIView):
    @swagger_auto_schema(
        tags=["auth"],
        responses={200: UserLoginDataSerializer()},
        request_body=login_schema,
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=request.data["email"], password=request.data["password"]
        )
        if not user:
            raise serializers.ValidationError(
                {"detail": "Incorrect email or password!"}
            )
        tokens = RefreshToken.for_user(user)
        return Response(
            UserLoginDataSerializer(
                {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "tokens": {
                        "access": str(tokens.access_token),
                        "refresh": str(tokens),
                    },
                }
            ).data
        )


class UserView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["auth"],
        response={200: UserSerializer()},
    )
    def get(self, request):
        user_id = request.auth.payload["user_id"]
        user = get_object_or_404(get_user_model(), pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ResetPasswordView(views.APIView):
    permission_classes = (AllowAny,)

    def create_link(self, user, request):
        uid64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        absolute_url = f"http://localhost:3000/auth/password-reset-confirm/{uid64}/{token}"

        return absolute_url

    def create_emaildata(self, user, absolute_url):
        email_body = (
            "Hi, \n Use link below to reset your password  \n" + absolute_url
        )

        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Reset your password",
        }
        return data

    @swagger_auto_schema(
        tags=["password", "reset"],
        responses={200: UserPasswordResetSerializer()},
    )
    def post(self, request):
        serializer = UserPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            link = self.create_link(user=user, request=request)
            data = self.create_emaildata(user=user, absolute_url=link)
            Util.send_email(data)

            return Response(
                {"message": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordConfirmView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserPasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )
