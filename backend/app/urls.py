"""
Main URL configuration for the NLQ backend project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 routes
    # All application-specific API endpoints will be rooted here.
    # path('api/v1/', include('app.api_v1_urls')), # This will be the pattern

    # API Schema (auto-generated documentation)
    # These endpoints are useful for developers and for generating client code.
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
