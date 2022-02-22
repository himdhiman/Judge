from rest_framework import serializers
from core import models


class LanguageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.Language
        fields = "__all__"
