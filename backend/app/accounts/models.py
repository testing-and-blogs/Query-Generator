from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model that extends the default Django user.
    This is the standard best practice for Django projects.
    """
    # Inherits username, first_name, last_name, email, is_staff, is_active, date_joined
    # from AbstractUser.

    # The spec requires a platform-level superadmin role.
    # `is_superuser` from AbstractUser can fill this role.
    # We add an explicit `is_superadmin` for clarity, which can just mirror is_superuser
    # or have its own logic. For now, we'll just add the field.
    is_superadmin = models.BooleanField(
        default=False,
        help_text='Designates that this user has all permissions without '
                  'explicitly assigning them. This is a platform-level role.'
    )

    def __str__(self):
        return self.email or self.username
