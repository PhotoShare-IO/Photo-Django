from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(allow_blank=False)
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
