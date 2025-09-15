from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Customize the User admin display.
    """
    # Add our custom field to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Platform Role', {'fields': ('is_superadmin',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Platform Role', {'fields': ('is_superadmin',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superadmin')
    list_filter = UserAdmin.list_filter + ('is_superadmin',)
