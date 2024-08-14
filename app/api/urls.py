from rest_framework.routers import DefaultRouter
from api import views
router = DefaultRouter()
router.register("application",views.ApplicationModelViewSet,"application")
router.register("template_config",views.TemplateConfigModelViewSet,"template_config")
urlpatterns = router.urls