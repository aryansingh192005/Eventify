from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models.deletion import ProtectedError

from notifications.utils import notify_event_created
from registrations.models import Registration

from .forms import EventCategoryForm, EventForm
from .models import Event, EventCategory


def get_dashboard_type(user):
    if user.is_superuser or user.role == "ADMIN":
        return "admin"
    elif user.role == "ORGANIZER":
        return "organizer"
    return "attendee"


def home(request):
    return render(
        request,
        "home.html",
    )


# ==========================================================
# CATEGORY LIST
# ==========================================================

@login_required
def category_list(request):

    if request.user.role != "ADMIN":
        messages.error(
            request,
            "You do not have permission to access this page.",
        )
        return redirect("dashboard_home")

    search = request.GET.get(
        "search",
        "",
    ).strip()

    categories = (
        EventCategory.objects
        .annotate(
            event_count=Count("events"),
        )
        .order_by("name")
    )

    if search:
        categories = categories.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
        )

    paginator = Paginator(
        categories,
        10,
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "events/category_list.html",
        {
    "page_obj": page_obj,
    "search": search,
    "dashboard_type": get_dashboard_type(request.user),
},
    )


# ==========================================================
# CREATE CATEGORY
# ==========================================================

@login_required
def category_create(request):

    if request.user.role != "ADMIN":
        messages.error(
            request,
            "You do not have permission to perform this action.",
        )
        return redirect("dashboard_home")

    if request.method == "POST":

        form = EventCategoryForm(
            request.POST,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Category created successfully.",
            )

            return redirect(
                "category_list",
            )

        

    else:

        form = EventCategoryForm()

    return render(
        request,
        "events/category_form.html",
        {
            "form": form,
            "title": "Add Category",
            "dashboard_type": get_dashboard_type(request.user),
        },
    )


# ==========================================================
# UPDATE CATEGORY
# ==========================================================

@login_required
def category_update(request, pk):

    if request.user.role != "ADMIN":
        messages.error(
            request,
            "You do not have permission to perform this action.",
        )
        return redirect("dashboard_home")

    category = get_object_or_404(
        EventCategory,
        pk=pk,
    )

    if request.method == "POST":

        form = EventCategoryForm(
            request.POST,
            instance=category,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Category updated successfully.",
            )

            return redirect(
                "category_list",
            )

    else:

        form = EventCategoryForm(
            instance=category,
        )

    return render(
        request,
        "events/category_form.html",
        {
            "form": form,
            "title": "Edit Category",
            "dashboard_type": get_dashboard_type(request.user),
        },
    )


# ==========================================================
# DELETE CATEGORY
# ==========================================================




@login_required
def category_delete(request, pk):

    if request.user.role != "ADMIN":
        messages.error(
            request,
            "You do not have permission to perform this action.",
        )
        return redirect("dashboard_home")

    category = get_object_or_404(
        EventCategory,
        pk=pk,
    )

    if request.method == "POST":

        try:

            category.delete()

            messages.success(
                request,
                "Category deleted successfully.",
            )

        except ProtectedError:

            messages.error(
                request,
                "Cannot delete this category because one or more events are using it. Delete or move those events first.",
            )

        return redirect("category_list")

    return render(
        request,
        "events/category_confirm_delete.html",
        {
            "category": category,
            "dashboard_type": get_dashboard_type(request.user),
        },
    )

    

# ==========================================================
# EVENT LIST
# ==========================================================

@login_required
def event_list(request):

    events = (
        Event.objects
        .select_related(
            "category",
            "organizer",
        )
        .annotate(
            registration_count=Count(
                "registrations",
                filter=Q(
                    registrations__status=Registration.Status.REGISTERED,
                ),
            ),
        )
    )

    search = request.GET.get(
        "search",
        "",
    ).strip()

    if search:

        events = events.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(venue__icontains=search)
            | Q(category__name__icontains=search)
            | Q(organizer__username__icontains=search)
        )

    category = request.GET.get(
        "category",
    )

    if category:

        events = events.filter(
            category_id=category,
        )

    status = request.GET.get(
        "status",
    )

    today = timezone.now()

    if status == "upcoming":

        events = events.filter(
            event_date__gte=today,
        )

    elif status == "past":

        events = events.filter(
            event_date__lt=today,
        )

    seats = request.GET.get(
        "seats",
    )

    if seats == "available":

        events = events.filter(
            available_seats__gt=0,
        )

    elif seats == "full":

        events = events.filter(
            available_seats=0,
        )

    sort = request.GET.get(
        "sort",
    )

    if sort == "oldest":

        events = events.order_by(
            "event_date",
        )

    elif sort == "title":

        events = events.order_by(
            "title",
        )

    elif sort == "popular":

        events = events.order_by(
            "-registration_count",
            "-event_date",
        )

    else:

        events = events.order_by(
            "-event_date",
        )

    paginator = Paginator(
        events,
        6,
    )

    page_obj = paginator.get_page(
        request.GET.get("page"),
    )

    categories = (
        EventCategory.objects
        .order_by("name")
    )

    return render(
    request,
    "events/event_list.html",
    {
        "events": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "selected_status": status,
        "selected_seats": seats,
        "selected_sort": sort,
        "dashboard_type": get_dashboard_type(request.user),
    },
)


# ==========================================================
# EVENT DETAIL
# ==========================================================

@login_required
def event_detail(request, slug):

    event = get_object_or_404(
        Event.objects.select_related(
            "category",
            "organizer",
        ),
        slug=slug,
    )

    registrations_count = (
        Registration.objects.filter(
            event=event,
            status=Registration.Status.REGISTERED,
        ).count()
    )

    related_events = Event.objects.filter(
    category=event.category
).exclude(
    id=event.id
).order_by(
    "-created_at"
)[:3]

    context = {
    "event": event,
    "registrations_count": registrations_count,
    "dashboard_type": get_dashboard_type(request.user),
    "related_events": related_events,
}

    return render(
        request,
        "events/event_detail.html",
        context,
    )


# ==========================================================
# CREATE EVENT
# ==========================================================

@login_required
def event_create(request):

    if request.user.role not in [
        "ADMIN",
        "ORGANIZER",
    ]:

        messages.error(
            request,
            "Only organizers can create events.",
        )

        return redirect(
            "event_list",
        )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            event = form.save(
                commit=False,
            )

            event.organizer = request.user

            

            event.save()

            notify_event_created(
                event,
            )

            messages.success(
                request,
                "Event created successfully.",
            )

            return redirect("event_list")

    else:

        form = EventForm()

    return render(
        request,
        "events/event_form.html",
        {
    "form": form,
    "title": "Create Event",
    "dashboard_type": get_dashboard_type(request.user),
},
    )

    

# ==========================================================
# UPDATE EVENT
# ==========================================================

@login_required
def event_update(request, slug):

    event = get_object_or_404(
        Event,
        slug=slug,
    )

    if (
        request.user != event.organizer
        and request.user.role != "ADMIN"
    ):
        messages.error(
            request,
            "You do not have permission to edit this event.",
        )
        return redirect(
            "event_detail",
            slug=event.slug,
        )

    if request.method == "POST":

        old_capacity = event.max_capacity

        form = EventForm(
            request.POST,
            request.FILES,
            instance=event,
        )

        if form.is_valid():

            updated_event = form.save(
                commit=False,
            )

            capacity_difference = (
                updated_event.max_capacity - old_capacity
            )

            updated_event.available_seats += capacity_difference

            if updated_event.available_seats < 0:
                updated_event.available_seats = 0

            updated_event.save()

            messages.success(
                request,
                "Event updated successfully.",
            )

            return redirect(
                "event_detail",
                slug=updated_event.slug,
            )

    else:

        form = EventForm(
            instance=event,
        )

    return render(
        request,
        "events/event_form.html",
        {
    "form": form,
    "event": event,
    "title": "Edit Event",
    "dashboard_type": get_dashboard_type(request.user),
},
    )


# ==========================================================
# DELETE EVENT
# ==========================================================

@login_required
def event_delete(request, slug):

    event = get_object_or_404(
        Event,
        slug=slug,
    )

    if (
        request.user != event.organizer
        and request.user.role != "ADMIN"
    ):
        messages.error(
            request,
            "You do not have permission to delete this event.",
        )
        return redirect(
            "event_detail",
            slug=event.slug,
        )

    if request.method == "POST":

        event.delete()

        messages.success(
            request,
            "Event deleted successfully.",
        )

        return redirect(
            "my_events",
        )

    return render(
        request,
        "events/event_confirm_delete.html",
        {
    "event": event,
    "dashboard_type": get_dashboard_type(request.user),
},
    )


# ==========================================================
# MY EVENTS
# ==========================================================

@login_required
def my_events(request):

    if request.user.role == "ADMIN":

        events = (
            Event.objects
            .select_related(
                "category",
                "organizer",
            )
            .annotate(
                registration_count=Count(
                    "registrations",
                    filter=Q(
                        registrations__status=Registration.Status.REGISTERED,
                    ),
                ),
            )
            .order_by(
                "-event_date",
            )
        )

    else:

        events = (
            Event.objects
            .filter(
                organizer=request.user,
            )
            .select_related(
                "category",
            )
            .annotate(
                registration_count=Count(
                    "registrations",
                    filter=Q(
                        registrations__status=Registration.Status.REGISTERED,
                    ),
                ),
            )
            .order_by(
                "-event_date",
            )
        )

    stats = events.aggregate(
        total_events=Count("id"),
        total_available_seats=Sum("available_seats"),
    )

    total_registrations = (
        Registration.objects.filter(
            event__in=events,
            status=Registration.Status.REGISTERED,
        ).count()
    )

    active_events = (
        events.filter(
            registration_deadline__gte=timezone.now(),
            available_seats__gt=0,
            status=Event.Status.PUBLISHED,
        ).count()
    )

    upcoming_events = (
        events.filter(
            event_date__gte=timezone.localdate(),
        ).count()
    )

    completed_events = (
        events.filter(
            event_date__lt=timezone.localdate(),
        ).count()
    )

    context = {
        "events": events,
        "total_events": stats["total_events"] or 0,
        "total_available_seats": stats["total_available_seats"] or 0,
        "total_registrations": total_registrations,
        "active_events": active_events,
        "upcoming_events": upcoming_events,
        "completed_events": completed_events,
        "dashboard_type": get_dashboard_type(request.user),
    }

    return render(
        request,
        "events/my_events.html",
        context,
    )