from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django’s base user.
    We'll use this for both Youth and Employer profiles.
    """

    USER_TYPE_CHOICES = [
        ("youth", "Youth"),
        ("employer", "Employer"),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default="youth",
        help_text="Select whether this user is a Youth or an Employer.",
    )

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class UserProfile(models.Model):
    """
    Base profile for all users (youth and employers can extend this later).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
