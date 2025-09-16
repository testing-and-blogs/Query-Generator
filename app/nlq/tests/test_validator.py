import pytest
from ..services.validator import SQLValidator, InvalidSQLError

def test_validator_allows_simple_select():
    sql = "SELECT id, name FROM users WHERE id = 1;"
    validator = SQLValidator(sql)
    assert validator.validate() is True

def test_validator_rejects_update():
    sql = "UPDATE users SET name = 'hacker' WHERE id = 1;"
    with pytest.raises(InvalidSQLError, match="Only SELECT statements are allowed"):
        SQLValidator(sql).validate()

def test_validator_rejects_drop():
    sql = "DROP TABLE users;"
    with pytest.raises(InvalidSQLError, match="Only SELECT statements are allowed"):
        SQLValidator(sql).validate()

def test_validator_rejects_multiple_statements():
    sql = "SELECT * FROM users; DROP TABLE users;"
    with pytest.raises(InvalidSQLError, match="Invalid SQL syntax"):
        SQLValidator(sql).validate()

def test_validator_rejects_forbidden_function():
    sql = "SELECT pg_sleep(10);"
    with pytest.raises(InvalidSQLError, match="Forbidden function call found: pg_sleep"):
        SQLValidator(sql, dialect='postgres').validate()

def test_validator_allows_safe_function():
    sql = "SELECT COUNT(*) FROM users;"
    validator = SQLValidator(sql)
    assert validator.validate() is True
