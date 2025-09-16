from django.urls import path
from .views import UserCreateAPIView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('login/', obtain_auth_token, name='user-login'),
]
