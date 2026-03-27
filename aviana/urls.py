from django.urls import path

from aviana.views import health, ping

urlpatterns = [
    path("health/", health),
    path("ping/", ping),
]
