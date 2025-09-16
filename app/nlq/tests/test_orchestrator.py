import pytest
from ..services.orchestrator import LLMOrchestrator
from app.connections.models import Connection
from app.schema_registry.models import SchemaCache
from app.queries.models import PromptExample
from app.tenancy.models import Tenant
from app.accounts.models import User

pytestmark = pytest.mark.django_db

@pytest.fixture
def connection_with_schema_and_examples():
    """Fixture for a connection with a cached schema and few-shot examples."""
    tenant = Tenant.objects.create(name="Test Tenant")
    user = User.objects.create_user(username="testuser")
    connection = Connection.objects.create(
        tenant=tenant,
        name="Test DB",
        driver="postgres",
        created_by=user
    )
    SchemaCache.objects.create(
        connection=connection,
        tenant=tenant,
        payload_json={'tables': [{'name': 'users', 'columns': [{'name': 'id'}, {'name': 'email'}]}]},
        graph_json={},
        hash='hash1'
    )
    PromptExample.objects.create(
        connection=connection,
        tenant=tenant,
        question="How many users?",
        sql="SELECT count(*) FROM users;"
    )
    return connection

def test_orchestrator_builds_prompt_correctly(connection_with_schema_and_examples):
    """
    Test that the LLM orchestrator constructs the system prompt with all context.
    """
    connection = connection_with_schema_and_examples
    prompt = "Show me all users."

    orchestrator = LLMOrchestrator(connection=connection, prompt=prompt)
    system_prompt = orchestrator._build_system_prompt()

    # Check for dialect
    assert "You are an expert PostgreSQL data analyst." in system_prompt

    # Check for schema context
    assert "--- Database Schema ---" in system_prompt
    assert "Table users: (id, email)" in system_prompt

    # Check for few-shot examples
    assert "--- Examples ---" in system_prompt
    assert "Question: How many users?" in system_prompt
    assert "SQL: SELECT count(*) FROM users;" in system_prompt
