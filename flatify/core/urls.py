from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('complete/<str:task_type>/', views.complete_task, name='complete_task'),
]