import sqlglot
from sqlglot import exp

class InvalidSQLError(ValueError):
    """Custom exception for validation errors."""
    pass

class SQLValidator:
    """
    Validates a SQL query to ensure it is safe to execute.
    """
    FORBIDDEN_DML = (exp.Insert, exp.Update, exp.Delete, exp.Truncate)
    FORBIDDEN_DDL = (exp.Drop, exp.Create, exp.Alter)

    FORBIDDEN_FUNCTIONS = (
        'xp_cmdshell',
        'pg_sleep',
    )

    def __init__(self, sql: str, dialect: str = 'tsql'):
        self.sql = sql
        self.dialect = dialect
        self.expression = self._parse()

    def _parse(self):
        try:
            # We expect only a single SQL statement.
            return sqlglot.parse_one(self.sql, read=self.dialect)
        except sqlglot.errors.ParseError as e:
            raise InvalidSQLError(f"Invalid SQL syntax: {e}")

    def validate(self):
        """
        Runs all validation checks.
        """
        # Check for forbidden top-level statements first
        if isinstance(self.expression, self.FORBIDDEN_DML):
             raise InvalidSQLError("DML statements are not allowed.")

        if isinstance(self.expression, self.FORBIDDEN_DDL):
             raise InvalidSQLError("DDL statements are not allowed.")

        # If it's not one of the forbidden types, it must be a SELECT.
        if not isinstance(self.expression, exp.Select):
            raise InvalidSQLError("Only SELECT statements are allowed.")

        # Finally, check for any forbidden functions within the query.
        for func in self.expression.find_all(exp.Func):
            if func.this.name.lower() in self.FORBIDDEN_FUNCTIONS:
                raise InvalidSQLError(f"Forbidden function call found: {func.this.name}")

        return True
