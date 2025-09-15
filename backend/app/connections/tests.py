import pytest
from app.tenancy.models import Tenant
from app.accounts.models import User
from .models import Connection

pytestmark = pytest.mark.django_db

def test_create_connection():
    """
    Tests the basic creation of a Connection model instance.
    """
    tenant = Tenant.objects.create(name="Test Tenant")
    user = User.objects.create_user(username="testuser")

    connection = Connection.objects.create(
        tenant=tenant,
        name="My Test Postgres DB",
        driver=Connection.Driver.POSTGRES,
        host="localhost",
        port=5432,
        database="testdb",
        username="testuser",
        created_by=user
    )

    # Set the password using the property setter
    connection.password = "mysecretpassword"
    connection.save()

    assert Connection.objects.count() == 1
    assert connection.tenant == tenant
    assert connection.name == "My Test Postgres DB"
    # The placeholder encryption adds a prefix, so we test for that
    assert connection.secret_encrypted.startswith("encrypted(")
    assert connection.password.startswith("decrypted(")
