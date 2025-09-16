from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from app.tenancy.models import Tenant, Membership
from django.conf import settings

class TenantMiddleware:
    """
    This middleware identifies the tenant based on the 'X-Tenant-ID' header
    and attaches it to the request object. It also ensures that the
    authenticated user is a member of the specified tenant.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # The admin interface and auth routes should not be tenant-scoped.
        if request.path.startswith('/admin/') or request.path.startswith('/api/v1/auth/'):
            return self.get_response(request)

        tenant_id = request.headers.get(settings.TENANT_HEADER)

        if not tenant_id:
            # For now, we allow requests without a tenant header to pass through,
            # but in a strict multi-tenant app, you might want to deny them.
            # Views will be responsible for handling requests without a tenant.
            request.tenant = None
            return self.get_response(request)

        try:
            tenant = Tenant.objects.get(id=tenant_id)
        except (Tenant.DoesNotExist, ValueError):
            raise PermissionDenied("Invalid tenant ID provided.")

        # Ensure the authenticated user is a member of this tenant.
        # This is a critical security check.
        if not request.user.is_authenticated:
             raise PermissionDenied("Authentication required.")

        if not Membership.objects.filter(user=request.user, tenant=tenant).exists():
            if not request.user.is_superadmin: # Allow superadmins to access any tenant
                raise PermissionDenied("You are not a member of this tenant.")

        request.tenant = tenant
        response = self.get_response(request)
        return response
