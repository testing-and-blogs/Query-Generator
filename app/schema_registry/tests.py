import pytest
from unittest.mock import patch, MagicMock
from .tasks import introspect_connection_task
from .models import SchemaCache
from app.connections.models import Connection
from app.tenancy.models import Tenant
from app.accounts.models import User

pytestmark = pytest.mark.django_db

@pytest.fixture
def connection_obj():
    """Fixture for a Connection object."""
    tenant = Tenant.objects.create(name="Test Tenant")
    user = User.objects.create_user(username="testuser")
    connection = Connection.objects.create(
        tenant=tenant,
        name="Test DB",
        driver="postgres",
        created_by=user
    )
    return connection

@patch('app.schema_registry.tasks.inspect')
@patch('app.schema_registry.tasks.create_engine')
def test_introspect_connection_task(mock_create_engine, mock_sqlalchemy_inspect, connection_obj):
    """
    Unit test the introspection task with mocked database interactions.
    """
    # --- Mock Setup ---
    # Mock the SQLAlchemy Inspector to return a predefined schema
    mock_inspector = MagicMock()
    mock_inspector.get_table_names.return_value = ['users']
    mock_inspector.get_columns.return_value = [
        {'name': 'id', 'type': 'INTEGER', 'nullable': False},
        {'name': 'email', 'type': 'VARCHAR(255)', 'nullable': False},
    ]
    mock_inspector.get_pk_constraint.return_value = {'constrained_columns': ['id']}
    mock_inspector.get_foreign_keys.return_value = []
    mock_sqlalchemy_inspect.return_value = mock_inspector

    # --- Task Execution ---
    introspect_connection_task(connection_obj.id)

    # --- Assertions ---
    # Check that a SchemaCache entry was created
    assert SchemaCache.objects.count() == 1
    cache = SchemaCache.objects.get(connection=connection_obj)

    # Check the content of the cached payload
    assert len(cache.payload_json['tables']) == 1
    assert cache.payload_json['tables'][0]['name'] == 'users'
    assert len(cache.payload_json['tables'][0]['columns']) == 2
    assert cache.payload_json['tables'][0]['columns'][0]['name'] == 'id'

    # Check the content of the graph
    assert len(cache.graph_json['nodes']) == 1
    assert cache.graph_json['nodes'][0]['id'] == 'users'
    assert len(cache.graph_json['edges']) == 0

    # Check that the hash is not empty
    assert cache.hash is not None
