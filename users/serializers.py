from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)
    username = serializers.CharField(allow_blank=False)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)

    def create(self, validated_data) -> get_user_model():
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        if any([first_name, last_name]):
            if not first_name or not last_name:
                raise serializers.ValidationError(
                    "First and last names are required!"
                )
        user = get_user_model().objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data.get("first_name", None),
            last_name=validated_data.get("last_name", None),
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class UserLoginDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    tokens = TokenSerializer()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)


class UserPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True
    )
    token = serializers.CharField(min_length=1, write_only=True)
    uid64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uid64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uid64 = attrs.get("uid64")

            id = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    "The reset link is invalid", 401
                )

            user.set_password(password)
            user.save()

            return user
        except Exception:
            raise serializers.ValidationError("The reset link is invalid", 401)
