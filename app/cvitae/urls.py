from django.contrib import admin
from django.urls import path, include

# don't change order to keep correct redirects
urlpatterns = [
    path("admin/", admin.site.urls),
    path("llm/collector/", include("llm.urls")),
    path("", include("api.urls")),
]
