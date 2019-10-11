from django.urls import path
from django.http import JsonResponse

from . import views

urlpatterns = [
    path('v1/user/create', views.create_user, name='create_user'),
    path('v1/tasks/scrap', views.tasks, name='tasks'),
    path('v1/categories/', views.get_categories, name='get_categories'),
    path('v1/book/id/<int:ide>', views.get_book, name='get_book_id'),
    path('v1/book/upc/<ide>', views.get_book, name='get_book_upc'),
]