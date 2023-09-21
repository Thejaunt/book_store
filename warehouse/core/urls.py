from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("w-admin/", admin.site.urls),
    path("", include("management.urls"))
]
