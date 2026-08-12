from django.conf import settings
from django.core.mail import send_mail

from .models import Notification


def send_notification_email(
    recipient,
    subject,
    message,
):
    """
    Send an email notification to a user.

    Returns True if the email was sent successfully.
    """

    if not recipient.email:
        return False

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient.email],
        fail_silently=True,
    )

    return True


def create_notification(
    recipient,
    title,
    message,
    notification_type=Notification.Type.GENERAL,
    url="",
    send_email=False,
    email_subject=None,
    email_message=None,
):
    """
    Create an in-app notification and optionally
    send an email notification.
    """

    notification = Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        url=url,
    )

    if send_email:

        send_notification_email(
            recipient=recipient,
            subject=email_subject or title,
            message=email_message or message,
        )

    return notification


def notify_event_created(event):
    """
    Notify the organizer that an event has been created.
    """

    subject = f"Event Created: {event.title}"

    message = (
        f"Hello {event.organizer.get_full_name() or event.organizer.username},\n\n"
        f'Your event "{event.title}" has been created successfully.\n\n'
        f"Venue: {event.venue}\n"
        f"Date: {event.event_date}\n\n"
        "Thank you for using the Event Management System."
    )

    return create_notification(
        recipient=event.organizer,
        title="Event Created",
        message=f'"{event.title}" has been created successfully.',
        notification_type=Notification.Type.EVENT_CREATED,
        url=event.get_absolute_url(),
        send_email=True,
        email_subject=subject,
        email_message=message,
    )


def notify_registration(event, attendee):
    """
    Notify the organizer about a new registration.
    """

    attendee_name = (
        attendee.get_full_name()
        or attendee.username
    )

    subject = f"New Registration for {event.title}"

    message = (
        f"Hello {event.organizer.get_full_name() or event.organizer.username},\n\n"
        f"{attendee_name} has registered for your event.\n\n"
        f"Event: {event.title}\n"
        f"Venue: {event.venue}\n"
        f"Date: {event.event_date}\n\n"
        "Please log in to view registration details."
    )

    return create_notification(
        recipient=event.organizer,
        title="New Registration",
        message=f"{attendee_name} registered for {event.title}.",
        notification_type=Notification.Type.EVENT_REGISTERED,
        url=event.get_absolute_url(),
        send_email=True,
        email_subject=subject,
        email_message=message,
    )


def notify_registration_cancelled(event, attendee):
    """
    Notify the organizer when a registration
    has been cancelled.
    """

    attendee_name = (
        attendee.get_full_name()
        or attendee.username
    )

    subject = f"Registration Cancelled for {event.title}"

    message = (
        f"Hello {event.organizer.get_full_name() or event.organizer.username},\n\n"
        f"{attendee_name} cancelled their registration.\n\n"
        f"Event: {event.title}\n"
        f"Venue: {event.venue}\n"
        f"Date: {event.event_date}\n\n"
        "Your available seats have been updated."
    )

    return create_notification(
        recipient=event.organizer,
        title="Registration Cancelled",
        message=f"{attendee_name} cancelled their registration for {event.title}.",
        notification_type=Notification.Type.EVENT_CANCELLED,
        url=event.get_absolute_url(),
        send_email=True,
        email_subject=subject,
        email_message=message,
    )


def notify_attendee_registration(event, attendee):
    """
    Send confirmation to the attendee after
    successful registration.
    """

    subject = f"Registration Confirmed: {event.title}"

    message = (
        f"Hello {attendee.get_full_name() or attendee.username},\n\n"
        f"You have successfully registered for:\n\n"
        f"Event: {event.title}\n"
        f"Venue: {event.venue}\n"
        f"Date: {event.event_date}\n"
        f"Time: {event.start_time} - {event.end_time}\n\n"
        "We look forward to seeing you!"
    )

    return create_notification(
        recipient=attendee,
        title="Registration Successful",
        message=f"You have successfully registered for {event.title}.",
        notification_type=Notification.Type.EVENT_REGISTERED,
        url=event.get_absolute_url(),
        send_email=True,
        email_subject=subject,
        email_message=message,
    )


def notify_attendee_cancellation(event, attendee):
    """
    Send confirmation after registration
    cancellation.
    """

    subject = f"Registration Cancelled: {event.title}"

    message = (
        f"Hello {attendee.get_full_name() or attendee.username},\n\n"
        f"Your registration for '{event.title}' has been cancelled successfully.\n\n"
        f"Venue: {event.venue}\n"
        f"Date: {event.event_date}\n\n"
        "Thank you for using the Event Management System."
    )

    return create_notification(
        recipient=attendee,
        title="Registration Cancelled",
        message=f"Your registration for {event.title} has been cancelled.",
        notification_type=Notification.Type.EVENT_CANCELLED,
        url=event.get_absolute_url(),
        send_email=True,
        email_subject=subject,
        email_message=message,
    )