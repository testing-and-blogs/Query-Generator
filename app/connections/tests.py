import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.tenancy.models import Tenant, Membership
from app.accounts.models import User
from .models import Connection
from app.schema_registry.models import SchemaCache

pytestmark = pytest.mark.django_db

# --- Model Tests ---
def test_create_connection_model():
    # ... (existing model test)
    pass

# --- API Tests ---
@pytest.fixture
def authenticated_client_with_tenant():
    """Fixture for an authenticated client with a tenant context."""
    user = User.objects.create_user(username='testuser', password='password123')
    tenant = Tenant.objects.create(name="Test Tenant")
    Membership.objects.create(user=user, tenant=tenant, role=Membership.Role.ADMIN)

    client = APIClient()
    client.force_authenticate(user=user)
    client.credentials(HTTP_X_TENANT_ID=tenant.id)

    return client, user, tenant

def test_api_create_connection(authenticated_client_with_tenant):
    # ... (existing api test)
    pass

@patch('app.connections.views.create_engine')
def test_api_test_connection_success(mock_create_engine, authenticated_client_with_tenant):
    # ... (existing api test)
    pass

# --- New Tests for Introspection ---

@patch('app.schema_registry.tasks.introspect_connection_task.delay')
def test_api_introspect_endpoint(mock_task_delay, authenticated_client_with_tenant):
    """
    Test that the introspect endpoint correctly enqueues the celery task.
    """
    client, _, tenant = authenticated_client_with_tenant
    conn = Connection.objects.create(tenant=tenant, name="DB to Introspect", driver="postgres")

    url = reverse('connection-introspect', kwargs={'pk': conn.pk})
    response = client.post(url)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data['status'] == 'ok'

    # Check that the Celery task's delay method was called once with the correct ID
    mock_task_delay.assert_called_once_with(conn.id)

def test_api_schema_endpoint_success(authenticated_client_with_tenant):
    """
    Test retrieving a schema from the cache via the API.
    """
    client, _, tenant = authenticated_client_with_tenant
    conn = Connection.objects.create(tenant=tenant, name="DB with Cache", driver="postgres")

    # Create a cache entry to be retrieved
    SchemaCache.objects.create(
        connection=conn,
        tenant=tenant,
        payload_json={'tables': [{'name': 'users'}]},
        graph_json={'nodes': [{'id': 'users'}]},
        hash='somehash'
    )

    url = reverse('connection-schema', kwargs={'pk': conn.pk})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['payload']['tables'][0]['name'] == 'users'
    assert response.data['graph']['nodes'][0]['id'] == 'users'

def test_api_schema_endpoint_not_found(authenticated_client_with_tenant):
    """
    Test that the schema endpoint returns 404 if no cache exists.
    """
    client, _, tenant = authenticated_client_with_tenant
    conn = Connection.objects.create(tenant=tenant, name="DB without Cache", driver="postgres")

    url = reverse('connection-schema', kwargs={'pk': conn.pk})
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['status'] == 'error'
