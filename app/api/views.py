from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from api import serializers

# Create your views here.


class PDFRenderer(BrowsableAPIRenderer):
    template = "application.html"
    format = "app"

class PDFCVRenderer(BrowsableAPIRenderer):
    template = "application_cv.html"
    format = "cv"

class PDFLetterRenderer(BrowsableAPIRenderer):
    template = "application_letter.html"
    format = "letter"

class EditRenderer(BrowsableAPIRenderer):
    template = "application_edit.html"
    format = "edit"

class SlimApiRenderer(BrowsableAPIRenderer):
    format = "slim"


class ApplicationModelViewSet(ModelViewSet):
    serializer_class = serializers.ApplicationModelSerializer
    renderer_classes = [
        SlimApiRenderer,
        BrowsableAPIRenderer,
        PDFRenderer,
        PDFCVRenderer,
        PDFLetterRenderer,
        EditRenderer,
        JSONRenderer,
    ]

    def get_serializer_class(self):
        if self.action in ["update"]:
            return serializers.ApplicationSlimModelSerializer
        if self.request.GET.get("format") in ["slim"]:
            return serializers.ApplicationSlimModelSerializer
        elif self.request.GET.get("format") in ["edit"]:
            return serializers.ApplicationEditModelSerializer
        elif self.action in ["list"]:
            return serializers.ApplicationSlimModelSerializer
        return self.serializer_class
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    

class TemplateConfigModelViewSet(ModelViewSet):
    serializer_class = serializers.TemplateConfigModelSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()