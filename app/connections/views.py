from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from sqlalchemy import create_engine, text
from .models import Connection
from .serializers import ConnectionSerializer
from app.schema_registry.models import SchemaCache
from app.schema_registry.tasks import introspect_connection_task

class ConnectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing database Connections.
    All operations are scoped to the current tenant.
    """
    serializer_class = ConnectionSerializer

    def get_queryset(self):
        """
        This view should only return connections for the current tenant.
        """
        if self.request.tenant:
            return Connection.objects.filter(tenant=self.request.tenant)
        return Connection.objects.none() # No tenant, no connections

    def perform_create(self, serializer):
        """
        Automatically associate the connection with the current tenant and user.
        """
        serializer.save(tenant=self.request.tenant, created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def test(self, request):
        """
        A custom action to test a database connection without saving it.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # ... (test logic remains the same as before)
        return Response({'status': 'ok', 'message': 'Connection successful'})

    @action(detail=True, methods=['post'])
    def introspect(self, request, pk=None):
        """
        Triggers the schema introspection Celery task for a connection.
        """
        connection = self.get_object() # Gets the connection instance
        task = introspect_connection_task.delay(connection.id)
        return Response({'status': 'ok', 'message': 'Introspection task started', 'task_id': task.id}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'])
    def schema(self, request, pk=None):
        """
        Retrieves the cached schema for a connection.
        """
        connection = self.get_object()
        try:
            schema_cache = SchemaCache.objects.get(connection=connection)
            return Response({
                'payload': schema_cache.payload_json,
                'graph': schema_cache.graph_json,
                'refreshed_at': schema_cache.refreshed_at
            })
        except SchemaCache.DoesNotExist:
            return Response({'status': 'error', 'message': 'Schema not found. Please run introspection first.'}, status=status.HTTP_404_NOT_FOUND)
