from celery import shared_task
from sqlalchemy import create_engine, inspect, text
from app.connections.models import Connection
from .models import SchemaCache
import hashlib

def get_db_url(conn: Connection) -> str:
    """Helper function to build a SQLAlchemy URL from a Connection object."""
    password = conn.password # Decrypts the password
    if conn.driver == 'postgres':
        return f"postgresql+psycopg://{conn.username}:{password}@{conn.host}:{conn.port}/{conn.database}"
    elif conn.driver == 'mysql':
        return f"mysql+pymysql://{conn.username}:{password}@{conn.host}:{conn.port}/{conn.database}"
    elif conn.driver == 'mssql':
        return f"mssql+pyodbc://{conn.username}:{password}@{conn.host}:{port}/{conn.database}?driver=ODBC+Driver+17+for+SQL+Server"
    elif conn.driver == 'sqlite':
        return f"sqlite:///{conn.database}"
    raise ValueError(f"Unsupported driver: {conn.driver}")

@shared_task
def introspect_connection_task(connection_id: int):
    """
    A Celery task to perform schema introspection on a given database connection.
    """
    try:
        connection_obj = Connection.objects.get(id=connection_id)
    except Connection.DoesNotExist:
        # Handle case where connection might have been deleted
        return f"Connection with id {connection_id} not found."

    db_url = get_db_url(connection_obj)
    engine = create_engine(db_url, connect_args={'connect_timeout': 10})
    inspector = inspect(engine)

    schema_payload = {
        'tables': []
    }
    graph_nodes = []
    graph_edges = []

    table_names = inspector.get_table_names()

    for table_name in table_names:
        columns = []
        for col in inspector.get_columns(table_name):
            columns.append({
                'name': col['name'],
                'type': str(col['type']),
                'nullable': col['nullable'],
                'default': col.get('default'),
            })

        primary_keys = inspector.get_pk_constraint(table_name).get('constrained_columns', [])
        foreign_keys = []
        for fk in inspector.get_foreign_keys(table_name):
            foreign_keys.append({
                'constrained_columns': fk['constrained_columns'],
                'referred_table': fk['referred_table'],
                'referred_columns': fk['referred_columns'],
            })
            # Add edge for the ERD graph
            graph_edges.append({
                'source': table_name,
                'target': fk['referred_table'],
                'label': f"{','.join(fk['constrained_columns'])} -> {','.join(fk['referred_columns'])}"
            })

        schema_payload['tables'].append({
            'name': table_name,
            'columns': columns,
            'primary_keys': primary_keys,
            'foreign_keys': foreign_keys,
        })
        # Add node for the ERD graph
        graph_nodes.append({'id': table_name, 'label': table_name})

    # Create a hash of the payload to detect changes
    payload_str = str(schema_payload)
    schema_hash = hashlib.sha256(payload_str.encode()).hexdigest()

    # Update or create the cache
    SchemaCache.objects.update_or_create(
        connection=connection_obj,
        defaults={
            'tenant': connection_obj.tenant,
            'payload_json': schema_payload,
            'graph_json': {'nodes': graph_nodes, 'edges': graph_edges},
            'hash': schema_hash,
        }
    )

    return f"Introspection complete for connection: {connection_obj.name}"
