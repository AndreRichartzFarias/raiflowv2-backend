from django.urls import path
from . import views
from .views import api_root

urlpatterns = [
    path('set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('user', views.user, name='user'),
    path('register', views.register, name='register'),
]