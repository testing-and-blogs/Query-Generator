from django.contrib import admin
from .models import Tenant, Membership

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan', 'created_at')
    search_fields = ('name',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant', 'role')
    list_filter = ('tenant', 'role')
    search_fields = ('user__username', 'tenant__name')
    autocomplete_fields = ('user', 'tenant')
