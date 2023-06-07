from rest_framework import serializers
from .models import DumbModel


class DumbSerializer(serializers.ModelSerializer):
    class Meta:
        model = DumbModel
        fields = "__all__"
