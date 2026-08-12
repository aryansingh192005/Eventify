from django.conf import settings
from django.db import models
from django.urls import reverse


class Notification(models.Model):

    class Type(models.TextChoices):
        EVENT_CREATED = "EVENT_CREATED", "Event Created"
        EVENT_UPDATED = "EVENT_UPDATED", "Event Updated"
        EVENT_REGISTERED = "EVENT_REGISTERED", "Event Registered"
        EVENT_CANCELLED = "EVENT_CANCELLED", "Event Cancelled"
        GENERAL = "GENERAL", "General"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=200,
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=50,
        choices=Type.choices,
        default=Type.GENERAL,
    )

    url = models.CharField(
        max_length=300,
        blank=True,
    )

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=[
                    "recipient",
                    "is_read",
                ]
            ),
            models.Index(
                fields=[
                    "-created_at",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"

    def get_absolute_url(self):

        if self.url:

            return self.url

        return reverse("notification_list")

    @property
    def icon(self):

        icons = {

            self.Type.EVENT_CREATED:
                "bi-calendar-plus",

            self.Type.EVENT_UPDATED:
                "bi-pencil-square",

            self.Type.EVENT_REGISTERED:
                "bi-ticket-perforated",

            self.Type.EVENT_CANCELLED:
                "bi-x-circle",

            self.Type.GENERAL:
                "bi-bell",

        }

        return icons.get(
            self.notification_type,
            "bi-bell",
        )


    @property
    def color(self):

        colors = {

            self.Type.EVENT_CREATED:
                "success",

            self.Type.EVENT_UPDATED:
                "primary",

            self.Type.EVENT_REGISTERED:
                "info",

            self.Type.EVENT_CANCELLED:
                "danger",

            self.Type.GENERAL:
                "secondary",

        }

        return colors.get(
            self.notification_type,
            "secondary",
        )