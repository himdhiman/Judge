from django.urls import path
from core import views

urlpatterns = [
    path("health_check/", views.HealthCheck.as_view()),
    path("execute_code/", views.ExecuteCode.as_view()),
]
