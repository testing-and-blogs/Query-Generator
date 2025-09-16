import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.accounts.models import User
from app.tenancy.models import Tenant, Membership
from app.connections.models import Connection

pytestmark = pytest.mark.django_db

@pytest.fixture
def tenants_and_users():
    """
    Fixture to create two separate tenants and a user for each.
    """
    # Tenant A setup
    tenant_a = Tenant.objects.create(name="Tenant A")
    user_a = User.objects.create_user(username="user_a", password="password123")
    Membership.objects.create(user=user_a, tenant=tenant_a)

    # Tenant B setup
    tenant_b = Tenant.objects.create(name="Tenant B")
    user_b = User.objects.create_user(username="user_b", password="password123")
    Membership.objects.create(user=user_b, tenant=tenant_b)

    return tenant_a, user_a, tenant_b, user_b

def test_user_cannot_access_other_tenant_resources(tenants_and_users):
    """
    This is a critical test to ensure tenant isolation.
    It verifies that a user logged into Tenant A cannot access resources
    that belong to Tenant B.
    """
    tenant_a, user_a, tenant_b, user_b = tenants_and_users

    # Create a resource that belongs to Tenant B
    connection_b = Connection.objects.create(
        tenant=tenant_b,
        name="Tenant B's Database",
        driver=Connection.Driver.POSTGRES,
        created_by=user_b
    )

    client = APIClient()
    client.force_authenticate(user=user_a) # Authenticate as User A

    # Set the tenant header for User A's requests
    client.credentials(HTTP_X_TENANT_ID=tenant_a.id)

    # Try to access a detail view for the resource from Tenant B
    url = reverse('connection-detail', kwargs={'pk': connection_b.pk})
    response = client.get(url)

    # The expected outcome is a 404 Not Found, because the ViewSet's queryset
    # is filtered by the tenant on the request.
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Also test the list view
    list_url = reverse('connection-list')
    list_response = client.get(list_url)

    assert list_response.status_code == status.HTTP_200_OK
    assert len(list_response.data) == 0 # No connections for Tenant A
