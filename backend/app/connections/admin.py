from django.contrib import admin
from .models import Connection

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    """
    Admin interface for the Connection model.
    """
    list_display = ('name', 'tenant', 'driver', 'host', 'database', 'username', 'is_active', 'created_at')
    list_filter = ('tenant', 'driver', 'is_active')
    search_fields = ('name', 'tenant__name', 'host', 'database', 'username')

    # The raw encrypted secret should not be editable directly.
    # A custom form would be used to handle password input.
    readonly_fields = ('secret_encrypted', 'created_at', 'updated_at')

    # Group fields into logical sections in the admin form.
    fieldsets = (
        (None, {
            'fields': ('name', 'tenant', 'driver', 'is_active')
        }),
        ('Connection Details', {
            'fields': ('host', 'port', 'database', 'username')
        }),
        ('Security', {
            'fields': ('secret_encrypted',)
        }),
        ('Metadata', {
            'fields': ('options_json', 'created_by', 'created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        # Prefetch related tenant to avoid extra queries.
        return super().get_queryset(request).select_related('tenant')
