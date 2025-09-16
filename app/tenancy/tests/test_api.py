import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.accounts.models import User
from app.tenancy.models import Tenant, Membership

# Mark all tests in this module as Django DB tests
pytestmark = pytest.mark.django_db

@pytest.fixture
def authenticated_client():
    """
    Fixture to create and authenticate a user and return an API client.
    """
    user = User.objects.create_user(username='testuser', password='password123')
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user

def test_create_tenant(authenticated_client):
    """
    Ensure an authenticated user can create a new tenant.
    """
    client, user = authenticated_client
    url = reverse('tenant-list')
    data = {'name': 'My New Tenant'}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Tenant.objects.count() == 1

    # Verify the creator is now an admin member of the new tenant
    tenant = Tenant.objects.get()
    assert Membership.objects.filter(tenant=tenant, user=user, role=Membership.Role.ADMIN).exists()

def test_list_tenants_shows_only_member_tenants(authenticated_client):
    """
    Ensure the tenant list endpoint only returns tenants the user is a member of.
    """
    client, user = authenticated_client

    # Create a tenant the user is a member of
    tenant1 = Tenant.objects.create(name="Tenant 1")
    Membership.objects.create(tenant=tenant1, user=user, role=Membership.Role.USER)

    # Create a tenant the user is NOT a member of
    tenant2 = Tenant.objects.create(name="Tenant 2")

    url = reverse('tenant-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == "Tenant 1"

def test_add_member_to_tenant(authenticated_client):
    """
    Ensure a tenant admin can add another user to their tenant.
    """
    client, admin_user = authenticated_client

    # Create a tenant where the authenticated user is an admin
    tenant = Tenant.objects.create(name="Admin's Tenant")
    Membership.objects.create(tenant=tenant, user=admin_user, role=Membership.Role.ADMIN)

    # Create another user to be added
    other_user = User.objects.create_user(username='otheruser', password='password123')

    # URL for adding members to the tenant
    url = reverse('tenant-membership-list', kwargs={'tenant_pk': tenant.pk})
    data = {'user_id': other_user.id, 'role': Membership.Role.USER}

    # Set the tenant header for the middleware
    client.credentials(HTTP_X_TENANT_ID=tenant.id)

    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Membership.objects.filter(tenant=tenant, user=other_user).exists()
