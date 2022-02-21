from django.urls import path
from core import views

urlpatterns = [
    path("execute/", views.ExecuteCode.as_view()),
    path("health_check/", views.HealthCheck.as_view()),
]
