from rest_framework import serializers
from .models import Tenant, Membership
from app.accounts.serializers import UserSerializer

class TenantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tenant model.
    """
    class Meta:
        model = Tenant
        fields = ('id', 'name', 'plan', 'created_at')


class MembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for the Membership model.
    Includes nested representation of the user.
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Membership
        fields = ('id', 'tenant', 'user', 'user_id', 'role')
        # The tenant will be set from the URL, so it's read-only here.
        read_only_fields = ('tenant',)
