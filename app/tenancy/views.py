from rest_framework import viewsets, permissions
from .models import Tenant, Membership
from .serializers import TenantSerializer, MembershipSerializer

class TenantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tenants to be viewed or edited.
    """
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This queryset should be filtered based on the user's memberships.
        A user should only be able to see tenants they are a member of.
        """
        # In a real implementation, the TenantManager would handle this filtering
        # based on the request.user. For now, we return all tenants created by the user.
        # This will be improved when the TenantMiddleware is in place.
        return Tenant.objects.filter(membership_set__user=self.request.user)

    def perform_create(self, serializer):
        """
        When a user creates a tenant, they automatically become an admin member.
        """
        tenant = serializer.save()
        Membership.objects.create(tenant=tenant, user=self.request.user, role=Membership.Role.ADMIN)


class MembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing memberships within a specific tenant.
    """
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated] # Should be more restrictive (e.g., Tenant Admin only)

    def get_queryset(self):
        """
        Filter memberships to the tenant specified in the URL.
        """
        tenant_pk = self.kwargs['tenant_pk']
        return Membership.objects.filter(tenant__pk=tenant_pk)

    def perform_create(self, serializer):
        """
        Associate the new membership with the tenant from the URL.
        """
        tenant_pk = self.kwargs['tenant_pk']
        tenant = Tenant.objects.get(pk=tenant_pk)
        # TODO: Add permission check to ensure request.user is an admin of this tenant.
        serializer.save(tenant=tenant)
