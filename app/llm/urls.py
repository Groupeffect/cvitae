from django.urls import path, include
from llm.views import collector
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("client", collector.LLMClientModelViewSet, "collector_client")
router.register("preface", collector.PromptPrefaceModelViewSet, "collector_preface")
router.register("prompt", collector.PromptClientModelViewSet, "collector_prompt")
urlpatterns = router.urls
