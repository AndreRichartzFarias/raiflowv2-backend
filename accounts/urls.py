from django.urls import path
from .views import LoginView, LogoutView, csrf_view, MeView

urlpatterns = [
    path('api/csrf/', csrf_view, name='api-csrf'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/me/', MeView.as_view(), name='api-me'),
]