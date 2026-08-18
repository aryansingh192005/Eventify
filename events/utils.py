from datetime import datetime

from django.utils import timezone

from .models import Event


def update_completed_events():

    today = timezone.localdate()

    events = Event.objects.filter(
        status=Event.Status.PUBLISHED,
        event_date__lte=today,
    )

    now = timezone.now()

    for event in events:

        event_end = timezone.make_aware(
            datetime.combine(
                event.event_date,
                event.end_time,
            ),
            timezone.get_current_timezone(),
        )

        if event_end <= now:

            event.status = Event.Status.COMPLETED

            event.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )