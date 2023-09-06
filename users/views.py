from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import views, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    UserSerializer,
    UserLoginDataSerializer,
    UserLoginSerializer,
)
from .swagger import register_schema, login_schema


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
