from .models import Notification


def notification_context(request):
    """
    Makes unread notification count available
    in all templates.
    """

    if (
        request.user.is_authenticated
        and hasattr(request.user, "notifications")
    ):

        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).count()

    else:

        unread_count = 0

    return {
        "unread_notification_count": unread_count,
    }