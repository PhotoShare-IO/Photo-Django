from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import views, serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    AuthUserSerializer,
    UserSerializer,
    UserLoginSerializer,
    RegisterUserSerializer,
)
from .swagger import register_schema, login_schema


class RegistrationView(views.APIView):
    @swagger_auto_schema(
        tags=["Auth"],
        responses={200: UserSerializer},
        request_body=register_schema,
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(RegisterUserSerializer({"user": user}).data)


class LoginView(views.APIView):
    @swagger_auto_schema(
        tags=["Auth"],
        responses={200: AuthUserSerializer},
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
            AuthUserSerializer(
                {
                    "user": user,
                    "tokens": {
                        "access": str(tokens.access_token),
                        "refresh": str(tokens),
                    },
                }
            ).data
        )


class UserAPI(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["User"],
        responses={200: RegisterUserSerializer},
    )
    def get(self, request, pk=None):
        UserModel = get_user_model()
        user = get_object_or_404(UserModel, pk=pk)
        serializer = RegisterUserSerializer({"user": user}).data
        return Response(serializer, status=status.HTTP_200_OK)
