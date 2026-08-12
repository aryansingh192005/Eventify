from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for the Event Management System.
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ORGANIZER = "ORGANIZER", "Organizer"
        ATTENDEE = "ATTENDEE", "Attendee"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ATTENDEE,
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.get_full_name() or self.username