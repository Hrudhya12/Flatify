from django.urls import path
from .views import dashboard, complete_task

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('complete/<str:task_type>/', complete_task, name='complete_task'),
]
