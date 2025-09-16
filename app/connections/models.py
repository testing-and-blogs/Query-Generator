from django.db import models
from django.conf import settings
from app.tenancy.models import TenantModel
from app.common.crypto import encrypt, decrypt

class Connection(TenantModel):
    """
    Stores connection details for a user's database.
    This model is tenant-scoped.
    """
    class Driver(models.TextChoices):
        POSTGRES = 'postgres', 'PostgreSQL'
        MYSQL = 'mysql', 'MySQL/MariaDB'
        SQLITE = 'sqlite', 'SQLite'
        MSSQL = 'mssql', 'Microsoft SQL Server'

    name = models.CharField(max_length=255)
    driver = models.CharField(max_length=20, choices=Driver.choices)
    host = models.CharField(max_length=255, blank=True, null=True)
    port = models.PositiveIntegerField(blank=True, null=True)
    database = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)

    # This field stores the encrypted password or full connection string.
    secret_encrypted = models.TextField(
        blank=True,
        help_text="Stores the encrypted database password or other sensitive connection info."
    )

    options_json = models.JSONField(
        default=dict,
        help_text="Optional JSON for extra connection parameters."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_connections'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        # A tenant should not have two connections with the same name.
        unique_together = ('tenant', 'name')

    def __str__(self):
        return f"{self.name} ({self.get_driver_display()})"

    @property
    def password(self):
        """
        A property to safely access the decrypted password.
        """
        if not self.secret_encrypted:
            return ""
        return decrypt(self.secret_encrypted)

    @password.setter
    def password(self, raw_password: str):
        """
        A property to safely set the encrypted password.
        """
        if not raw_password:
            self.secret_encrypted = ""
        else:
            self.secret_encrypted = encrypt(raw_password)
