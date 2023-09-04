from rest_framework import serializers


class AlbumSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    file_url = serializers.URLField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    album = AlbumSerializer()
