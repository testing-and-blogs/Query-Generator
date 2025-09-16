from celery import shared_task
from sqlalchemy import create_engine, text
from django.conf import settings
from .models import QueryHistory
from app.schema_registry.tasks import get_db_url # Re-use the helper

@shared_task
def execute_query_task(query_history_id: int):
    """
    A Celery task to execute a validated SQL query against a user's database.
    """
    try:
        query_history = QueryHistory.objects.select_related('connection').get(id=query_history_id)
    except QueryHistory.DoesNotExist:
        return f"QueryHistory with id {query_history_id} not found."

    connection_obj = query_history.connection
    db_url = get_db_url(connection_obj)

    # Add a LIMIT to the query to prevent fetching too much data
    # This is a simple implementation. A more robust one would use sqlglot to parse
    # and safely add the limit clause.
    sql_to_run = query_history.generated_sql
    if "limit" not in sql_to_run.lower():
        sql_to_run = f"{sql_to_run.rstrip(';')} LIMIT {settings.RESULT_MAX_ROWS};"

    try:
        # Connect with statement-level timeout
        timeout_sec = settings.QUERY_TIMEOUT_MS / 1000
        engine = create_engine(db_url, connect_args={'connect_timeout': timeout_sec})

        with engine.connect() as connection:
            # For postgres, we can set a statement timeout
            if connection_obj.driver == 'postgres':
                connection.execute(text(f"SET statement_timeout = {settings.QUERY_TIMEOUT_MS}"))

            result = connection.execute(text(sql_to_run))

            # Fetch results and convert to a list of dicts
            results_as_dict = [row._asdict() for row in result]

            # Update history object
            query_history.status = QueryHistory.Status.OK
            query_history.row_count = len(results_as_dict)
            # In a real app, you'd store the results somewhere (e.g., S3, Redis)
            # and just save a reference here. Storing large results in the DB is bad.
            # For now, we'll just log success.
            # query_history.results = results_as_dict

    except Exception as e:
        query_history.status = QueryHistory.Status.ERROR
        query_history.error_text = str(e)

    query_history.save()

    return f"Execution finished for QueryHistory id {query_history_id} with status {query_history.status}"
