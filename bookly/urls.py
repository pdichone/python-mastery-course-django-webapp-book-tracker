from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bookly_nest.urls")),
    path("accounts/", include("accounts.urls")),
]
