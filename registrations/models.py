import uuid

from django.conf import settings
from django.db import models

from events.models import Event


class Registration(models.Model):

    class Status(models.TextChoices):

        REGISTERED = "REGISTERED", "Registered"

        CANCELLED = "CANCELLED", "Cancelled"

        ATTENDED = "ATTENDED", "Attended"


    # =====================================
    # USER / EVENT RELATION
    # =====================================

    attendee = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="registrations",

    )


    event = models.ForeignKey(

        Event,

        on_delete=models.CASCADE,

        related_name="registrations",

    )


    # =====================================
    # REGISTRATION DETAILS
    # =====================================

    registration_date = models.DateTimeField(

        auto_now_add=True,

    )


    status = models.CharField(

        max_length=20,

        choices=Status.choices,

        default=Status.REGISTERED,

    )


    # =====================================
    # QR TICKET SYSTEM
    # =====================================

    ticket_code = models.UUIDField(

        default=uuid.uuid4,

        unique=True,

        editable=False,

        help_text="Unique QR ticket identifier",

    )


    ticket_qr = models.ImageField(

        upload_to="tickets/qr/",

        blank=True,

        null=True,

        help_text="Generated QR code for this ticket",

    )


    # =====================================
    # EVENT CHECK-IN SYSTEM
    # =====================================

    checked_in = models.BooleanField(

        default=False,

        help_text="Whether attendee has entered the event",

    )


    checked_in_at = models.DateTimeField(

        null=True,

        blank=True,

    )


    # =====================================
    # META
    # =====================================

    class Meta:

        ordering = [

            "-registration_date"

        ]


        constraints = [

            models.UniqueConstraint(

                fields=[

                    "attendee",

                    "event",

                ],

                name="unique_event_registration",

            )

        ]


        indexes = [

            models.Index(

                fields=[

                    "ticket_code",

                ]

            ),

            models.Index(

                fields=[

                    "attendee",

                    "status",

                ]

            ),

            models.Index(

                fields=[

                    "event",

                    "status",

                ]

            ),

        ]


    # =====================================
    # METHODS
    # =====================================

    def __str__(self):

        return f"{self.attendee.username} - {self.event.title}"


    def ticket_id(self):

        """
        Short readable ticket ID
        """

        return str(
            self.ticket_code
        )[:8].upper()


    def is_valid_ticket(self):

        """
        Check if ticket can be used for entry.
        """

        return (

            self.status == self.Status.REGISTERED

            and not self.checked_in

        )