from django.urls import path
from .views import NLQAPIView

urlpatterns = [
    path('nlq/', NLQAPIView.as_view(), name='nlq'),
]
