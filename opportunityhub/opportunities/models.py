from django.db import models
from employers.models import EmployerProfile


class Skill(models.Model):
    """
    Skills that can be associated with opportunities and youth profiles
    """

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Opportunity(models.Model):
    """
    Job opportunities, gigs, and internships posted by employers
    """

    CATEGORY_CHOICES = [
        ("Technology", "Technology"),
        ("Agriculture", "Agriculture"),
        ("Healthcare", "Healthcare"),
        ("Education", "Education"),
        ("Construction", "Construction"),
        ("Hospitality", "Hospitality"),
        ("Finance", "Finance"),
        ("Marketing", "Marketing"),
        ("Sales", "Sales"),
        ("Other", "Other"),
    ]

    OPPORTUNITY_TYPE_CHOICES = [
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
        ("Contract", "Contract"),
        ("Internship", "Internship"),
        ("Freelance", "Freelance"),
        ("Gig", "Gig"),
    ]

    EXPERIENCE_CHOICES = [
        ("Entry Level", "Entry Level"),
        ("1-2 years", "1-2 years"),
        ("3-5 years", "3-5 years"),
        ("5+ years", "5+ years"),
    ]

    employer = models.ForeignKey(
        EmployerProfile, on_delete=models.CASCADE, related_name="opportunities"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    opportunity_type = models.CharField(max_length=50, choices=OPPORTUNITY_TYPE_CHOICES)
    county = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    required_skills = models.ManyToManyField(
        Skill, related_name="opportunities", blank=True
    )
    experience_required = models.CharField(
        max_length=50, choices=EXPERIENCE_CHOICES, default="Entry Level"
    )
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum salary in KES",
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum salary in KES",
    )
    application_deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.employer.company_name}"
