from django.db import models
from django.conf import settings
from app.tenancy.models import TenantModel
from app.connections.models import Connection

class QueryHistory(TenantModel):
    """
    Logs a record of every natural language prompt and its corresponding
    SQL execution for a user.
    """
    class Status(models.TextChoices):
        OK = 'OK', 'OK'
        ERROR = 'ERROR', 'Error'
        TIMEOUT = 'TIMEOUT', 'Timeout'

    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    prompt = models.TextField()
    generated_sql = models.TextField(blank=True)
    exec_status = models.CharField(max_length=10, choices=Status.choices)
    row_count = models.PositiveIntegerField(null=True, blank=True)
    duration_ms = models.PositiveIntegerField(help_text="Execution duration in milliseconds.")
    error_text = models.TextField(blank=True, null=True)

    # created_at is inherited from TenantModel

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Query Histories"

    def __str__(self):
        return f"Query by {self.user} at {self.created_at}"


class PromptExample(TenantModel):
    """
    Stores a "few-shot" example of a good question-to-SQL pair for a
    specific database connection, used to improve LLM accuracy.
    """
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    sql = models.TextField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Example for {self.connection.name}: {self.question}"
