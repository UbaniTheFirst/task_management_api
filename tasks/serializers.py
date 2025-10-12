from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        """Check that passwords match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs
    
    def create(self, validated_data):
        """Create user with encrypted password."""
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Task
        fields = [
            'id', 'user', 'title', 'description', 'due_date',
            'priority', 'status', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['completed_at', 'created_at', 'updated_at', 'status']
    
    def validate_due_date(self, value):
        """Ensure due_date is in the future."""
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
    
    def validate(self, attrs):
        """Prevent editing completed tasks."""
        if self.instance and self.instance.status == 'Completed':
            raise serializers.ValidationError(
                "Cannot edit a completed task. Mark it as incomplete first."
            )
        return attrs


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating tasks."""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
    
    def validate_due_date(self, value):
        """Ensure due_date is in the future."""
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value