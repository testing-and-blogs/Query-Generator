from rest_framework_nested import routers
from .views import TenantViewSet, MembershipViewSet

# Create a router and register our viewsets with it.
router = routers.SimpleRouter()
router.register(r'tenants', TenantViewSet, basename='tenant')

# Create a nested router for memberships under tenants
memberships_router = routers.NestedSimpleRouter(router, r'tenants', lookup='tenant')
memberships_router.register(r'members', MembershipViewSet, basename='tenant-membership')

# The API URLs are now determined automatically by the router.
urlpatterns = router.urls + memberships_router.urls
