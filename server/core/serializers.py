from pyexpat import model
from rest_framework import serializers
from core import models


class LanguageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.Language
        fields = "__all__"

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Submission
        fields = "__all__"
