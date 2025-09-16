from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .services.orchestrator import LLMOrchestrator
from .services.validator import SQLValidator, InvalidSQLError
from app.connections.models import Connection
from app.queries.models import QueryHistory
from app.queries.tasks import execute_query_task

class NLQAPIView(APIView):
    """
    The main API View for the Natural Language to SQL flow.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        connection_id = request.data.get('connection_id')

        if not prompt or not connection_id:
            return Response({'error': 'prompt and connection_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure the connection belongs to the current tenant
            connection = Connection.objects.get(id=connection_id, tenant=request.tenant)
        except Connection.DoesNotExist:
            return Response({'error': 'Connection not found'}, status=status.HTTP_404_NOT_FOUND)

        # 1. Orchestrate LLM call
        orchestrator = LLMOrchestrator(connection=connection, prompt=prompt)
        generated_sql = orchestrator.generate_sql()

        # 2. Validate the generated SQL
        try:
            validator = SQLValidator(sql=generated_sql, dialect=connection.driver)
            validator.validate()
        except InvalidSQLError as e:
            # Log this failed validation for review
            QueryHistory.objects.create(
                tenant=request.tenant,
                connection=connection,
                user=request.user,
                prompt=prompt,
                generated_sql=generated_sql,
                status=QueryHistory.Status.ERROR,
                error_text=f"Validation Error: {e}"
            )
            return Response({'error': f'Generated SQL failed validation: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Create a history entry and enqueue the execution task
        history_entry = QueryHistory.objects.create(
            tenant=request.tenant,
            connection=connection,
            user=request.user,
            prompt=prompt,
            generated_sql=generated_sql,
            status='PENDING' # A 'PENDING' status would be useful here
        )

        task = execute_query_task.delay(history_entry.id)

        return Response({
            'status': 'ok',
            'message': 'Query is being executed',
            'generated_sql': generated_sql,
            'history_id': history_entry.id,
            'task_id': task.id
        }, status=status.HTTP_202_ACCEPTED)
