from django.urls import path, include

urlpatterns = [
    path('auth/', include('app.accounts.urls')),
    path('', include('app.tenancy.urls')),
    path('', include('app.connections.urls')),
    path('', include('app.nlq.urls')),
]
