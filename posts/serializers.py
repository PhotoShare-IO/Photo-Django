from rest_framework import serializers
from .models import PostModel, AlbumModel


class AlbumSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    file_url = serializers.URLField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    album = AlbumSerializer()


class PostCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    file_url = serializers.URLField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    album_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return PostModel.objects.create(**validated_data)
