from django.urls import path
from core import views

urlpatterns = [
    path("execute/", views.ExecuteCode.as_view()),
    path("health_check/", views.HealthCheck.as_view()),
    path("get_languages/", views.GetLanguages.as_view()),
    path("get_result/<str:task_id>/", views.GetResult.as_view()),
]
