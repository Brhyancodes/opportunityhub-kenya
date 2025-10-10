from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password2",
            "user_type",
            "phone_number",
            "location",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        """
        Check that passwords match
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Create user and associated profile
        """
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)

        # Create UserProfile automatically
        UserProfile.objects.create(user=user)

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "phone_number",
            "location",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for basic user profile
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "bio", "date_of_birth", "created_at"]
        read_only_fields = ["id", "created_at"]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint
    """

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password]
    )
