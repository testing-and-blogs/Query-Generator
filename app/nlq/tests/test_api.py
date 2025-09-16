import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.tenancy.models import Tenant, Membership
from app.accounts.models import User
from app.connections.models import Connection
from app.schema_registry.models import SchemaCache
from app.queries.models import QueryHistory

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client_with_tenant_and_connection():
    """Fixture for an authenticated client with tenant and connection setup."""
    user = User.objects.create_user(username='testuser', password='password123')
    tenant = Tenant.objects.create(name="Test Tenant")
    Membership.objects.create(user=user, tenant=tenant)
    connection = Connection.objects.create(tenant=tenant, name="Test DB", driver="postgres")
    SchemaCache.objects.create(connection=connection, tenant=tenant, payload_json={'tables': []})

    client = APIClient()
    client.force_authenticate(user=user)
    client.credentials(HTTP_X_TENANT_ID=tenant.id)

    return client, connection

@patch('app.queries.tasks.execute_query_task.delay')
@patch('app.nlq.views.LLMOrchestrator')
def test_nlq_api_flow(mock_orchestrator, mock_task_delay, api_client_with_tenant_and_connection):
    """
    Integration test for the full NLQ API flow, with mocking.
    """
    client, connection = api_client_with_tenant_and_connection

    # Configure mocks
    mock_orchestrator.return_value.generate_sql.return_value = "SELECT id FROM users;"

    # Make the API call
    url = reverse('nlq')
    data = {
        'prompt': 'Show me all users',
        'connection_id': connection.id
    }
    response = client.post(url, data, format='json')

    # Assertions
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data['status'] == 'ok'
    assert response.data['generated_sql'] == "SELECT id FROM users;"

    # Check that the orchestrator was initialized and used correctly
    mock_orchestrator.assert_called_once()
    mock_orchestrator.return_value.generate_sql.assert_called_once()

    # Check that a QueryHistory object was created
    assert QueryHistory.objects.count() == 1
    history = QueryHistory.objects.first()
    assert history.prompt == 'Show me all users'
    assert history.generated_sql == "SELECT id FROM users;"

    # Check that the Celery task was enqueued with the history ID
    mock_task_delay.assert_called_once_with(history.id)
