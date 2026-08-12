from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from events.models import Event
from registrations.models import Registration

from .forms import UserProfileForm, UserRegistrationForm
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            messages.success(
                request,
                f"Welcome back, {user.username}!",
            )
            return redirect("dashboard_home")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "accounts/login.html",
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully. You can now login.",
            )

            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


@login_required
def profile_view(request):
    user = request.user

    context = {
        "user_obj": user,
        "events_created": Event.objects.filter(
            organizer=user,
        ).count(),
        "events_registered": Registration.objects.filter(
            attendee=user,
        ).count(),
        "active_registrations": Registration.objects.filter(
            attendee=user,
            status=Registration.Status.REGISTERED,
        ).count(),
        "cancelled_registrations": Registration.objects.filter(
            attendee=user,
            status=Registration.Status.CANCELLED,
        ).count(),
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully.",
            )

            return redirect("profile")
    else:
        form = UserProfileForm(
            instance=request.user,
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )


@login_required
def logout_view(request):
    logout(request)
    messages.success(
        request,
        "You have been logged out successfully.",
    )
    return redirect("home")

# ==========================================================
# ADMIN USER MANAGEMENT
# ==========================================================

@login_required
def admin_user_list(request):

    # ------------------------------------------
    # ADMIN ONLY
    # ------------------------------------------

    if (
        not request.user.is_superuser
        and request.user.role != User.Role.ADMIN
    ):
        messages.error(
            request,
            "You do not have permission to manage users.",
        )

        return redirect("dashboard_home")


    users = User.objects.all()


    # ------------------------------------------
    # SEARCH
    # ------------------------------------------

    search = request.GET.get("search", "").strip()

    if search:

        users = users.filter(
            Q(username__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
        )


    # ------------------------------------------
    # ROLE FILTER
    # ------------------------------------------

    role = request.GET.get("role", "").strip()

    if role in [
        User.Role.ORGANIZER,
        User.Role.ATTENDEE,
        User.Role.ADMIN,
    ]:

        users = users.filter(
            role=role
        )


    # ------------------------------------------
    # STATUS FILTER
    # ------------------------------------------

    account_status = request.GET.get(
        "status",
        "",
    ).strip()


    if account_status == "active":

        users = users.filter(
            is_active=True
        )

    elif account_status == "inactive":

        users = users.filter(
            is_active=False
        )


    # ------------------------------------------
    # STATISTICS
    # ------------------------------------------

    total_users = User.objects.count()

    total_organizers = User.objects.filter(
        role=User.Role.ORGANIZER
    ).count()

    total_attendees = User.objects.filter(
        role=User.Role.ATTENDEE
    ).count()

    active_users = User.objects.filter(
        is_active=True
    ).count()

    inactive_users = User.objects.filter(
        is_active=False
    ).count()


    # ------------------------------------------
    # ORDERING
    # ------------------------------------------

    users = users.order_by(
        "first_name",
        "last_name",
        "username",
    )


    return render(
        request,
        "accounts/admin_user_list.html",
        {
            "users": users,

            "search": search,
            "selected_role": role,
            "selected_status": account_status,

            "total_users": total_users,
            "total_organizers": total_organizers,
            "total_attendees": total_attendees,
            "active_users": active_users,
            "inactive_users": inactive_users,

            "dashboard_type": "admin",
        },
    )


# ==========================================================
# USER DETAIL
# ==========================================================

@login_required
def admin_user_detail(request, user_id):

    if (
        not request.user.is_superuser
        and request.user.role != User.Role.ADMIN
    ):
        messages.error(
            request,
            "You do not have permission to manage users.",
        )

        return redirect("dashboard_home")


    user_obj = get_object_or_404(
        User,
        id=user_id,
    )


    events_created = Event.objects.filter(
        organizer=user_obj,
    ).count()


    registrations = Registration.objects.filter(
        attendee=user_obj,
    )


    total_registrations = registrations.count()


    active_registrations = registrations.filter(
        status=Registration.Status.REGISTERED,
    ).count()


    cancelled_registrations = registrations.filter(
        status=Registration.Status.CANCELLED,
    ).count()


    attended_registrations = registrations.filter(
        status=Registration.Status.ATTENDED,
    ).count()


    return render(
        request,
        "accounts/admin_user_detail.html",
        {
            "user_obj": user_obj,

            "events_created": events_created,

            "total_registrations": total_registrations,
            "active_registrations": active_registrations,
            "cancelled_registrations": cancelled_registrations,
            "attended_registrations": attended_registrations,

            "dashboard_type": "admin",
        },
    )


# ==========================================================
# ACTIVATE / DEACTIVATE
# ==========================================================

@login_required
def admin_user_toggle_status(request, user_id):

    if (
        not request.user.is_superuser
        and request.user.role != User.Role.ADMIN
    ):
        messages.error(
            request,
            "You do not have permission to manage users.",
        )

        return redirect("dashboard_home")


    user_obj = get_object_or_404(
        User,
        id=user_id,
    )


    # ------------------------------------------
    # PROTECT CURRENT ADMIN
    # ------------------------------------------

    if user_obj.id == request.user.id:

        messages.error(
            request,
            "You cannot deactivate your own account.",
        )

        return redirect(
            "admin_user_list",
        )


    user_obj.is_active = not user_obj.is_active

    user_obj.save(
        update_fields=[
            "is_active",
        ],
    )


    if user_obj.is_active:

        messages.success(
            request,
            f"{user_obj.username} has been activated.",
        )

    else:

        messages.warning(
            request,
            f"{user_obj.username} has been deactivated.",
        )


    return redirect(
        request.POST.get(
            "next",
            "admin_user_list",
        )
    )


# ==========================================================
# DELETE USER
# ==========================================================

@login_required
def admin_user_delete(request, user_id):

    if (
        not request.user.is_superuser
        and request.user.role != User.Role.ADMIN
    ):
        messages.error(
            request,
            "You do not have permission to manage users.",
        )

        return redirect("dashboard_home")


    user_obj = get_object_or_404(
        User,
        id=user_id,
    )


    # ------------------------------------------
    # PROTECT CURRENT ADMIN
    # ------------------------------------------

    if user_obj.id == request.user.id:

        messages.error(
            request,
            "You cannot delete your own account.",
        )

        return redirect(
            "admin_user_list",
        )


    if request.method != "POST":

        return render(
            request,
            "accounts/admin_user_delete.html",
            {
                "user_obj": user_obj,
                "dashboard_type": "admin",
            },
        )


    username = user_obj.username


    user_obj.delete()


    messages.success(
        request,
        f"User '{username}' has been deleted successfully.",
    )


    return redirect(
        "admin_user_list",
    )