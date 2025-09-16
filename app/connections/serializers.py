from rest_framework import serializers
from .models import Connection

class ConnectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Connection model.
    Handles the password field securely.
    """
    # The 'password' field is not a real model field, but a property.
    # We define it here to allow it to be used in the API for setting the password.
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Connection
        fields = (
            'id', 'name', 'driver', 'host', 'port', 'database', 'username',
            'password', 'options_json', 'is_active', 'created_at', 'updated_at'
        )
        # The tenant is set automatically from the request context, so it's not included here.
        # The created_by field is also set automatically.

    def create(self, validated_data):
        # Pop the password from the validated data if it exists
        raw_password = validated_data.pop('password', None)

        # Create the connection instance
        connection = Connection(**validated_data)

        # Set the password, which will trigger the encryption via the model's property setter
        if raw_password is not None:
            connection.password = raw_password

        connection.save()
        return connection

    def update(self, instance, validated_data):
        # Pop the password from the validated data if it exists
        raw_password = validated_data.pop('password', None)

        # Set the password on the instance if a new one was provided
        if raw_password is not None:
            instance.password = raw_password

        # Update the other fields on the instance
        return super().update(instance, validated_data)
