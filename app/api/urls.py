from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register("application", views.ApplicationModelViewSet, "application")
router.register("template_config", views.TemplateConfigModelViewSet, "template_config")
router.register("admin", views.AdminRedirectViewSet, "admin")
urlpatterns = router.urls
