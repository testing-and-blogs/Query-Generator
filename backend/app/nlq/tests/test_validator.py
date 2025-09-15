import pytest

# Assume a validator function exists, e.g., in `app.nlq.services.validator`
# from app.nlq.services.validator import validate_sql, InvalidSQLError

# Placeholder for the exception
class InvalidSQLError(Exception):
    pass

# Placeholder for the validator function
def validate_sql(sql):
    """
    A placeholder for the real SQL validator.
    This would use sqlglot to parse and inspect the AST.
    """
    # Simple checks for the placeholder
    lower_sql = sql.lower().strip()
    if not lower_sql.startswith('select'):
        raise InvalidSQLError("SQL must be a SELECT statement.")
    if 'delete from' in lower_sql or 'update ' in lower_sql or 'insert into' in lower_sql:
        raise InvalidSQLError("DML statements are not allowed.")
    if 'drop table' in lower_sql or 'create table' in lower_sql:
        raise InvalidSQLError("DDL statements are not allowed.")
    if sql.count(';') > 1:
        raise InvalidSQLError("Multiple statements are not allowed.")
    return True


def test_validator_allows_simple_select():
    """
    Ensures a basic, safe SELECT statement passes validation.
    """
    sql = "SELECT id, name FROM users WHERE id = 1;"
    assert validate_sql(sql) is True

def test_validator_rejects_update():
    """
    Ensures an UPDATE statement is rejected.
    """
    sql = "UPDATE users SET name = 'hacker' WHERE id = 1;"
    with pytest.raises(InvalidSQLError, match="DML statements are not allowed"):
        validate_sql(sql)

def test_validator_rejects_delete():
    """
    Ensures a DELETE statement is rejected.
    """
    sql = "DELETE FROM users;"
    with pytest.raises(InvalidSQLError, match="DML statements are not allowed"):
        validate_sql(sql)

def test_validator_rejects_drop():
    """
    Ensures a DROP TABLE statement is rejected.
    """
    sql = "DROP TABLE users;"
    with pytest.raises(InvalidSQLError, match="DDL statements are not allowed"):
        validate_sql(sql)

def test_validator_rejects_multiple_statements():
    """
    Ensures queries with multiple statements are rejected.
    """
    sql = "SELECT * FROM users; DROP TABLE users;"
    with pytest.raises(InvalidSQLError, match="Multiple statements are not allowed"):
        validate_sql(sql)

def test_validator_is_case_insensitive():
    """
    Ensures the validator checks are case-insensitive.
    """
    sql = "select * from users; drop table users;"
    with pytest.raises(InvalidSQLError, match="Multiple statements are not allowed"):
        validate_sql(sql)
