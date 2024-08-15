from rest_framework.viewsets import ModelViewSet
from llm.serializers import collector


class LLMClientModelViewSet(ModelViewSet):

    serializer_class = collector.LLMClientModelSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    def get_serializer_class(self):

        return super().get_serializer_class()


class PromptClientModelViewSet(ModelViewSet):

    serializer_class = collector.PromptClientModelSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    def get_serializer_class(self):

        return super().get_serializer_class()


class PromptPrefaceModelViewSet(ModelViewSet):

    serializer_class = collector.PromptPrefaceModelSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    def get_serializer_class(self):

        return super().get_serializer_class()
