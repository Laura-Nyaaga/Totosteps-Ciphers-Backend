from rest_framework import serializers
from django.contrib.auth.models import User
"""
This serializer is used to convert User model instances into JSON format and vice versa.
It is based on Django's `ModelSerializer`, which automatically handles the conversion between
model instances and primitive data types (such as JSON).
The `Meta` class defines the fields that should be included in the serialized output
 when retrieving or creating a user instance, including sensitive fields like `password`.
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']






