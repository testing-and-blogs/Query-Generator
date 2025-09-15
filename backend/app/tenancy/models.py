from django.db import models
from django.conf import settings

class Tenant(models.Model):
    """
    Represents a tenant in the multi-tenant system.
    Each tenant is an isolated workspace with its own users, connections, etc.
    """
    name = models.CharField(max_length=255, unique=True)
    plan = models.CharField(max_length=50, default='free')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# This is a placeholder for a custom manager that would automatically
# filter queries by tenant. This would be implemented in a separate file.
class TenantManager(models.Manager):
    def get_queryset(self):
        # In a real implementation, this would be tied to the current request's tenant.
        # For now, it returns all objects.
        return super().get_queryset()

class TenantModel(models.Model):
    """
    An abstract base model for all models that are scoped to a tenant.
    It automatically adds a `tenant` foreign key.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='%(class)s_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager() # The default manager.
    by_tenant = TenantManager() # The tenant-aware manager.

    class Meta:
        abstract = True
        # Enforce that all tenant-scoped models have unique constraints that include the tenant.
        # This is a good practice but must be defined on the child models.


class Membership(models.Model):
    """
    Links a User to a Tenant with a specific role.
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    class Meta:
        unique_together = ('tenant', 'user')

    def __str__(self):
        return f"{self.user} in {self.tenant} as {self.role}"
