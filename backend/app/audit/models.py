from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from app.tenancy.models import TenantModel

class AuditLog(TenantModel):
    """
    Records a significant event that occurred in the system for auditing purposes.
    This is a generic log that can point to any other object in the database.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The user who performed the action."
    )
    action = models.CharField(
        max_length=255,
        help_text="A description of the action performed (e.g., 'user_login', 'connection_create')."
    )

    # Generic foreign key to the object that was the target of the action.
    # For example, if a connection was created, this would point to the Connection object.
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    metadata_json = models.JSONField(
        default=dict,
        help_text="Extra details about the event (e.g., IP address, changed fields)."
    )

    # created_at is inherited from TenantModel

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Audit: {self.action} by {self.user} at {self.created_at}"
