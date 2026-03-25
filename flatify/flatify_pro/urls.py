from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from flatify.core.views import dashboard, complete_task

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('complete/<str:task_type>/', complete_task, name='complete_task'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('admin/', admin.site.urls),
]
