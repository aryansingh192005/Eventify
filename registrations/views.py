from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.utils import timezone
from events.views import get_dashboard_type
from events.models import Event
from notifications.utils import (
    notify_attendee_registration,
    notify_registration,
    notify_registration_cancelled,
    notify_attendee_cancellation,
)

from .models import Registration
from .utils import generate_ticket_qr

@login_required
def register_event(request, slug):

    with transaction.atomic():

        event = get_object_or_404(
    Event.objects.select_for_update(),
    slug=slug,
)

        if event.organizer == request.user:

            messages.error(
                request,
                "You cannot register for your own event.",
            )

            return redirect(
                "event_detail",
                slug=event.slug,
            )

        if not event.is_registration_open:

            messages.error(
                request,
                "Registration is closed.",
            )

            return redirect(
                "event_detail",
                slug=event.slug,
            )

        if event.available_seats <= 0:

            messages.error(
                request,
                "Sorry! No seats are available for this event.",
            )

            return redirect(
                "event_detail",
                slug=event.slug,
            )

        registration = (
            Registration.objects
            .filter(
                attendee=request.user,
                event=event,
            )
            .first()
        )

        if registration:

            if registration.status == Registration.Status.REGISTERED:

                messages.warning(
                    request,
                    "You are already registered for this event.",
                )

                return redirect(
                    "event_detail",
                    slug=event.slug,
                )

            registration.status = Registration.Status.REGISTERED

            registration.save(
                update_fields=[
                    "status",
                ],
            )

        else:

            registration = Registration.objects.create(
                attendee=request.user,
                event=event,
            )

        # Generate QR ticket
        if not registration.ticket_qr:
            generate_ticket_qr(
                registration,
            )

        event.available_seats = max(0, event.available_seats - 1)

        event.save(
            update_fields=[
                "available_seats",
            ],
        )

        notify_registration(
            event,
            request.user,
        )

        notify_attendee_registration(
            event,
            request.user,
        )

    messages.success(
        request,
        "Registration successful!",
    )

    return redirect(
        "event_detail",
        slug=event.slug,
    )

@login_required
def my_registrations(request):

    registrations = (
        Registration.objects
        .select_related(
            "event",
            "event__category",
            "event__organizer",
        )
        .filter(
            attendee=request.user,
        )
    )

    # =====================================
    # SEARCH
    # =====================================

    search = request.GET.get("search")

    if search:
        registrations = registrations.filter(
            Q(event__title__icontains=search) |
            Q(event__venue__icontains=search)
        )

    # =====================================
    # STATUS FILTER
    # Default = Registered
    # =====================================

    status = request.GET.get(
        "status",
        Registration.Status.REGISTERED
    )

    if status == Registration.Status.REGISTERED:

        registrations = registrations.filter(
            status=Registration.Status.REGISTERED
        )

    elif status == Registration.Status.CANCELLED:

        registrations = registrations.filter(
            status=Registration.Status.CANCELLED
        )

    elif status == Registration.Status.ATTENDED:

        registrations = registrations.filter(
            status=Registration.Status.ATTENDED
        )

    # =====================================
    # SORTING
    # =====================================

    sort = request.GET.get("sort", "latest")

    if sort == "oldest":

        registrations = registrations.order_by(
            "registration_date"
        )

    elif sort == "event":

        registrations = registrations.order_by(
            "event__title"
        )

    else:

        registrations = registrations.order_by(
            "-registration_date"
        )

    # =====================================
    # DASHBOARD STATS
    # (Calculated from ALL registrations)
    # =====================================

    all_registrations = Registration.objects.filter(
        attendee=request.user
    )

    total = all_registrations.count()

    active = all_registrations.filter(
        status=Registration.Status.REGISTERED
    ).count()

    cancelled = all_registrations.filter(
        status=Registration.Status.CANCELLED
    ).count()

    upcoming = all_registrations.filter(
        status=Registration.Status.REGISTERED,
        event__event_date__gte=timezone.now().date()
    ).count()

    # =====================================
    # RENDER
    # =====================================

    return render(
        request,
        "registrations/my_registrations.html",
        {
            "registrations": registrations,
            "dashboard_type": get_dashboard_type(request.user),

            "total_registrations": total,
            "active_registrations": active,
            "cancelled_registrations": cancelled,
            "upcoming_registrations": upcoming,

            "current_status": status,
            "search": search,
            "sort": sort,
        },
    )

@login_required
def cancel_registration(request, registration_id):

    with transaction.atomic():

        registration = get_object_or_404(
    Registration.objects
    .select_related("event")
    .select_for_update(),
    id=registration_id,
    attendee=request.user,
)

        if registration.status == Registration.Status.CANCELLED:

            messages.warning(
                request,
                "Registration is already cancelled.",
            )

            return redirect(
                "my_registrations",
            )

        registration.status = Registration.Status.CANCELLED

        registration.save(
            update_fields=[
                "status",
            ],
        )

        event = registration.event

        event.available_seats += 1

        event.save(
            update_fields=[
                "available_seats",
            ],
        )

        notify_registration_cancelled(
            event,
            request.user,
        )

        notify_attendee_cancellation(
            event,
            request.user,
        )

    messages.success(
        request,
        "Registration cancelled successfully.",
    )

    return redirect(
        "my_registrations",
    )

@login_required
def qr_checkin(request, slug):

    event = get_object_or_404(
        Event.objects.select_related("organizer"),
        slug=slug,
    )

    user = request.user

    # -----------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------

    is_admin = (
        user.is_superuser
        or getattr(user, "role", None) == user.Role.ADMIN
    )

    is_organizer = (
        getattr(user, "role", None) == user.Role.ORGANIZER
    )

    if not is_admin:

        if not is_organizer:
            messages.error(
                request,
                "You do not have permission to access event check-in.",
            )

            return redirect("dashboard_home")

        if event.organizer != user:
            messages.error(
                request,
                "You can only manage check-in for your own events.",
            )

            return redirect("dashboard_home")

    return render(
        request,
        "registrations/qr_checkin.html",
        {
            "event": event,
            "dashboard_type": get_dashboard_type(user),
        },
    )


@login_required
def verify_qr_checkin(request, slug):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request method.",
            },
            status=405,
        )

    event = get_object_or_404(
        Event.objects.select_related("organizer"),
        slug=slug,
    )

    user = request.user

    # -----------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------

    is_admin = (
        user.is_superuser
        or getattr(user, "role", None) == user.Role.ADMIN
    )

    is_organizer = (
        getattr(user, "role", None) == user.Role.ORGANIZER
    )

    if not is_admin:

        if not is_organizer:

            return JsonResponse(
                {
                    "success": False,
                    "message": "You do not have permission to perform check-in.",
                },
                status=403,
            )

        if event.organizer != user:

            return JsonResponse(
                {
                    "success": False,
                    "message": "You can only check in attendees for your own events.",
                },
                status=403,
            )

    # -----------------------------------------
    # GET SCANNED TICKET
    # -----------------------------------------

    ticket_code = request.POST.get("ticket_code", "").strip()

    if not ticket_code:

        return JsonResponse(
            {
                "success": False,
                "message": "No QR ticket was detected.",
            },
            status=400,
        )

    # -----------------------------------------
    # FIND REGISTRATION
    # -----------------------------------------

    try:

        registration = (
            Registration.objects
            .select_related(
                "attendee",
                "event",
            )
            .select_for_update()
            .get(
                ticket_code=ticket_code,
            )
        )

    except Registration.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid QR ticket. Registration not found.",
            },
            status=404,
        )

    # -----------------------------------------
    # VERIFY EVENT
    # -----------------------------------------

    if registration.event_id != event.id:

        return JsonResponse(
            {
                "success": False,
                "message": "This QR ticket belongs to another event.",
            },
            status=400,
        )

    # -----------------------------------------
    # VERIFY REGISTRATION STATUS
    # -----------------------------------------

    if registration.status == Registration.Status.CANCELLED:

        return JsonResponse(
            {
                "success": False,
                "message": "This registration has been cancelled.",
            },
            status=400,
        )

    if registration.status == Registration.Status.ATTENDED:

        checked_time = registration.checked_in_at

        checked_time_text = (
            timezone.localtime(
                checked_time
            ).strftime(
                "%d %b %Y, %I:%M %p"
            )
            if checked_time
            else "an earlier time"
        )

        return JsonResponse(
            {
                "success": False,
                "already_checked_in": True,
                "message": (
                    "This attendee has already been checked in."
                ),
                "checked_in_at": checked_time_text,
                "attendee": (
                    registration.attendee.get_full_name()
                    or registration.attendee.username
                ),
            },
            status=400,
        )

    # -----------------------------------------
    # VERIFY TICKET
    # -----------------------------------------

    if not registration.is_valid_ticket():

        return JsonResponse(
            {
                "success": False,
                "message": "This ticket is no longer valid.",
            },
            status=400,
        )

    # -----------------------------------------
    # MARK ATTENDANCE
    # -----------------------------------------

    with transaction.atomic():

        registration = (
            Registration.objects
            .select_for_update()
            .select_related(
                "attendee",
                "event",
            )
            .get(
                id=registration.id,
            )
        )

        if not registration.is_valid_ticket():

            return JsonResponse(
                {
                    "success": False,
                    "message": "This ticket is no longer valid.",
                },
                status=400,
            )

        registration.checked_in = True

        registration.checked_in_at = timezone.now()

        registration.status = Registration.Status.ATTENDED

        registration.save(
            update_fields=[
                "checked_in",
                "checked_in_at",
                "status",
            ],
        )

    attendee_name = (
        registration.attendee.get_full_name()
        or registration.attendee.username
    )

    checked_in_time = timezone.localtime(
        registration.checked_in_at
    ).strftime(
        "%d %b %Y, %I:%M %p"
    )

    return JsonResponse(
        {
            "success": True,

            "message": "Check-in successful.",

            "attendee": attendee_name,

            "event": registration.event.title,

            "ticket_id": registration.ticket_id(),

            "checked_in_at": checked_in_time,
        }
    )