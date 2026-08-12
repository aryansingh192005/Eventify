from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from events.views import get_dashboard_type
from .models import Notification
from django.views.decorators.http import require_POST

@login_required
def notification_list(request):

    notifications = (
        Notification.objects
        .filter(
            recipient=request.user,
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications,
            "dashboard_type": get_dashboard_type(request.user),
        },
    )


@require_POST
@login_required
def mark_notification_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user,
    )

    notification.is_read = True
    notification.save(update_fields=["is_read"])

    if notification.url:

        return redirect(notification.url)

    return redirect("notification_list")


@require_POST
@login_required
def mark_all_notifications_read(request):

    Notification.objects.filter(
        recipient=request.user,
        is_read=False,
    ).update(
        is_read=True,
    )

    return redirect("notification_list")