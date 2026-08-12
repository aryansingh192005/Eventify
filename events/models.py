from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class EventCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    icon = models.CharField(
        max_length=50,
        default="bi-calendar-event",
        help_text="Bootstrap Icon class",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events",
    )

    category = models.ForeignKey(
        EventCategory,
        on_delete=models.PROTECT,
        related_name="events",
    )

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField()

    venue = models.CharField(
        max_length=200,
    )

    image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True,
    )

    event_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    registration_deadline = models.DateTimeField()

    max_capacity = models.PositiveIntegerField()

    available_seats = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-event_date",
            "-start_time",
        ]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        if not self.pk:
            self.available_seats = self.max_capacity

        super().save(*args, **kwargs)

    @property
    def is_registration_open(self):
        return (
            self.status == self.Status.PUBLISHED
            and timezone.now() <= self.registration_deadline
            and self.available_seats > 0
        )

    @property
    def seats_filled(self):
        return self.max_capacity - self.available_seats

    @property
    def registration_percentage(self):
        if self.max_capacity == 0:
            return 0

        return int(
            (self.seats_filled / self.max_capacity) * 100
        )

    @property
    def is_full(self):
        return self.available_seats <= 0

    @property
    def is_upcoming(self):
        return self.event_date >= timezone.localdate()

    def get_absolute_url(self):
        return reverse(
            "event_detail",
            kwargs={
                "slug": self.slug,
            },
        )

    def __str__(self):
        return self.title