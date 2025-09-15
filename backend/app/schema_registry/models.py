from django.db import models
from app.tenancy.models import TenantModel
from app.connections.models import Connection

class SchemaCache(TenantModel):
    """
    Stores the cached result of a database schema introspection.
    This avoids having to re-introspect the database on every request.
    """
    connection = models.OneToOneField(
        Connection,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='schema_cache'
    )

    payload_json = models.JSONField(
        help_text="The full introspected schema: tables, columns, PKs, FKs, etc."
    )

    graph_json = models.JSONField(
        help_text="A lightweight graph representation (nodes and edges) for the ERD."
    )

    hash = models.CharField(
        max_length=64,
        help_text="A hash of the schema content to detect changes."
    )

    refreshed_at = models.DateTimeField(
        auto_now=True,
        help_text="The timestamp of the last successful introspection."
    )

    def __str__(self):
        return f"Schema for {self.connection.name}"
