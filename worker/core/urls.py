from django.urls import path
from core import views

urlpatterns = [path("health_check/", views.HealthCheck.as_view())]
