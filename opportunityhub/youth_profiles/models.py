from django.db import models
from accounts.models import User


class Skill(models.Model):
    """
    Represents a skill (e.g., Python, Graphic Design, Data Entry)
    """

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ("tech", "Technology"),
            ("design", "Design"),
            ("business", "Business"),
            ("trades", "Trades"),
            ("other", "Other"),
        ],
        default="other",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class YouthProfile(models.Model):
    """
    Extended profile for youth users
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="youth_profile",
        limit_choices_to={"user_type": "youth"},
    )

    # Personal Info
    age = models.PositiveIntegerField(null=True, blank=True)
    county = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    # Work Preferences
    WORK_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("freelance", "Freelance"),
        ("internship", "Internship"),
    ]
    preferred_work_type = models.CharField(
        max_length=20, choices=WORK_TYPE_CHOICES, default="full_time"
    )

    # Skills & Experience
    skills = models.ManyToManyField(Skill, through="YouthSkill", blank=True)
    education_level = models.CharField(
        max_length=50,
        choices=[
            ("secondary", "Secondary School"),
            ("certificate", "Certificate"),
            ("diploma", "Diploma"),
            ("degree", "Degree"),
            ("masters", "Masters"),
        ],
        blank=True,
    )
    years_of_experience = models.PositiveIntegerField(default=0)

    # Profile completeness
    profile_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Youth Profile: {self.user.username}"


class YouthSkill(models.Model):
    """
    Through model for Youth-Skill relationship with proficiency level
    """

    youth_profile = models.ForeignKey(YouthProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    PROFICIENCY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    ]
    proficiency = models.CharField(
        max_length=20, choices=PROFICIENCY_CHOICES, default="beginner"
    )
    years_of_experience = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["youth_profile", "skill"]

    def __str__(self):
        return f"{self.youth_profile.user.username} - {self.skill.name} ({self.proficiency})"


class Experience(models.Model):
    """
    Work experience entries for youth
    """

    youth_profile = models.ForeignKey(
        YouthProfile, on_delete=models.CASCADE, related_name="experiences"
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} at {self.company}"
