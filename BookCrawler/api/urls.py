from django.urls import path
from django.http import JsonResponse

from . import views

urlpatterns = [
    path('v1/tasks/scrap', views.tasks, name='tasks'),
]