from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register("application", views.ApplicationModelViewSet, basename="application")
router.register("template_config", views.TemplateConfigModelViewSet, basename="template_config")
router.register("admin", views.AdminRedirectViewSet, basename="admin")
urlpatterns = router.urls
