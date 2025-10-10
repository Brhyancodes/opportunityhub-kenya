from django.db import models
from accounts.models import User


class EmployerProfile(models.Model):
    """
    Extended profile for employer users
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employer_profile",
        limit_choices_to={"user_type": "employer"},
    )

    # Company Info
    company_name = models.CharField(max_length=200)
    company_description = models.TextField(blank=True)
    industry = models.CharField(
        max_length=100,
        choices=[
            ("tech", "Technology"),
            ("finance", "Finance"),
            ("education", "Education"),
            ("healthcare", "Healthcare"),
            ("retail", "Retail"),
            ("manufacturing", "Manufacturing"),
            ("agriculture", "Agriculture"),
            ("other", "Other"),
        ],
        default="other",
    )

    # Contact & Location
    company_website = models.URLField(blank=True)
    company_email = models.EmailField(blank=True)
    company_phone = models.CharField(max_length=15, blank=True)
    county = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    # Verification
    verified = models.BooleanField(default=False)
    verification_document = models.FileField(
        upload_to="employer_docs/", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Employer: {self.company_name}"
