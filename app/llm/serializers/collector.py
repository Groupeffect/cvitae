from rest_framework import serializers
from llm.database import collector


class LLMClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = collector.LLMClient
        fields = "__all__"


class PromptClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = collector.PromptClient
        fields = "__all__"


class PromptPrefaceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = collector.PromptPreface
        fields = "__all__"
