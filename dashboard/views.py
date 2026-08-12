from multiprocessing import context
from urllib import request

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from django.utils import timezone

import csv
import json


from events.models import Event
from accounts.models import User
from registrations.models import Registration





# =====================================================
# ROLE HELPERS
# =====================================================


def is_admin(user):

    return (
        user.is_authenticated
        and user.role == User.Role.ADMIN
    )



def is_organizer(user):

    return (
        user.is_authenticated
        and user.role == User.Role.ORGANIZER
    )



def is_attendee(user):

    return (
        user.is_authenticated
        and user.role == User.Role.ATTENDEE
    )







# =====================================================
# DASHBOARD ROUTER
# =====================================================


@login_required
def dashboard_home(request):

    user = request.user

    # Django superuser or admin role
    if user.is_superuser or user.role == User.Role.ADMIN:
        context = get_admin_dashboard_context()

    # Organizer
    elif user.role == User.Role.ORGANIZER:
        context = get_organizer_dashboard_context(request)

    # Attendee
    else:
        context = get_attendee_dashboard_context(request)
    context["hide_breadcrumb"] = True
    return render(
        request,
        "dashboard/home.html",
        context
    )




# =====================================================
# ADMIN DASHBOARD
# =====================================================


def get_admin_dashboard_context():



    total_users = User.objects.count()



    total_organizers = User.objects.filter(
        role=User.Role.ORGANIZER
    ).count()



    total_events = Event.objects.count()



    total_registrations = Registration.objects.count()






    published_events = Event.objects.filter(
        status=Event.Status.PUBLISHED
    ).count()



    pending_events = Event.objects.filter(
        status=Event.Status.DRAFT
    ).count()





    # Revenue calculation
    # Registration has no amount field.
    # Revenue = ticket price * registrations


    total_revenue = 0


    for registration in Registration.objects.select_related(
        "event"
    ):

        total_revenue += registration.event.price






    recent_events = (
        Event.objects
        .select_related(
            "organizer",
            "category"
        )
        .order_by(
            "-created_at"
        )[:5]
    )







    recent_registrations = (
        Registration.objects
        .select_related(
            "attendee",
            "event"
        )
        .order_by(
            "-registration_date"
        )[:5]
    )








    upcoming_event_list = (
        Event.objects
        .filter(
            event_date__gte=timezone.localdate()
        )
        .select_related(
            "organizer",
            "category"
        )
        .order_by(
            "event_date"
        )[:5]
    )







    chart_months = []

    event_chart_data = []

    registration_chart_data = []





    for month in range(1,13):


        chart_months.append(
            str(month)
        )



        event_chart_data.append(

            Event.objects.filter(
                created_at__month=month
            ).count()

        )



        registration_chart_data.append(

            Registration.objects.filter(
                registration_date__month=month
            ).count()

        )







    return {



        "dashboard_type":
            "admin",



        "total_users":
            total_users,



        "total_organizers":
            total_organizers,



        "total_events":
            total_events,



        "total_registrations":
            total_registrations,



        "published_events":
            published_events,



        "pending_events":
            pending_events,



        "total_revenue":
            total_revenue,



        "recent_events":
            recent_events,



        "recent_registrations":
            recent_registrations,



        "upcoming_event_list":
            upcoming_event_list,



        "chart_months":
            json.dumps(chart_months),



        "event_chart_data":
            json.dumps(event_chart_data),



        "registration_chart_data":
            json.dumps(registration_chart_data),


    }

    # =====================================================
# ORGANIZER DASHBOARD
# =====================================================


def get_organizer_dashboard_context(request):


    user = request.user




    organizer_events = Event.objects.filter(
        organizer=user
    )




    total_events = organizer_events.count()



    total_registrations = Registration.objects.filter(
        event__organizer=user
    ).count()





    upcoming_events = organizer_events.filter(
        event_date__gte=timezone.localdate()
    ).count()






    total_revenue = 0


    registrations = Registration.objects.filter(
        event__organizer=user
    ).select_related(
        "event"
    )



    for registration in registrations:

        total_revenue += registration.event.price






    recent_events = (

        organizer_events
        .order_by(
            "-created_at"
        )[:5]

    )






    recent_registrations = (

        Registration.objects
        .filter(
            event__organizer=user
        )
        .select_related(
            "attendee",
            "event"
        )
        .order_by(
            "-registration_date"
        )[:5]

    )







    upcoming_event_list = (

        organizer_events
        .filter(
            event_date__gte=timezone.localdate()
        )
        .order_by(
            "event_date"
        )[:10]

    )






    event_chart = []

    registration_chart = []

    chart_months = []





    for month in range(1,13):


        chart_months.append(
            str(month)
        )



        event_chart.append(

            organizer_events.filter(
                created_at__month=month
            ).count()

        )



        registration_chart.append(

            Registration.objects.filter(
                event__organizer=user,
                registration_date__month=month
            ).count()

        )








    return {


        "dashboard_type":
            "organizer",



        "total_events":
            total_events,



        "total_registrations":
            total_registrations,



        "upcoming_events":
            upcoming_events,



        "total_revenue":
            total_revenue,



        "recent_events":
            recent_events,



        "recent_registrations":
            recent_registrations,



        "upcoming_event_list":
            upcoming_event_list,



        "chart_months":
            json.dumps(chart_months),



        "event_chart_data":
            json.dumps(event_chart),



        "registration_chart_data":
            json.dumps(registration_chart),



        "event_chart":
            json.dumps(event_chart),



        "registration_chart":
            json.dumps(registration_chart),



    }












# =====================================================
# ATTENDEE DASHBOARD
# =====================================================


def get_attendee_dashboard_context(request):


    user = request.user




    user_registrations = Registration.objects.filter(
        attendee=user
    )





    total_registrations = (
        user_registrations.count()
    )






    active_registrations = (
        user_registrations
        .filter(
            status=Registration.Status.REGISTERED
        )
        .count()
    )








    upcoming_registrations = (

        user_registrations
        .filter(
            event__event_date__gte=
            timezone.localdate()
        )
        .select_related(
            "event"
        )
        .order_by(
            "event__event_date"
        )

    )







    available_events = Event.objects.filter(

        status=Event.Status.PUBLISHED,

        event_date__gte=timezone.localdate()

    ).count()







    recent_registrations = (

        user_registrations
        .select_related(
            "event"
        )
        .order_by(
            "-registration_date"
        )[:5]

    )






    upcoming_event_list = (

        Event.objects
        .filter(

            status=Event.Status.PUBLISHED,

            event_date__gte=
            timezone.localdate()

        )
        .exclude(
            organizer=user
        )
        .order_by(
            "event_date"
        )[:6]

    )







    return {


        "dashboard_type":
            "attendee",



        "total_registrations":
            total_registrations,



        "active_registrations":
            active_registrations,



        "upcoming_registrations":
            upcoming_registrations,



        "available_events":
            available_events,



        "recent_registrations":
            recent_registrations,



        "upcoming_event_list":
            upcoming_event_list,


    }

    # =====================================================
# REPORTS DASHBOARD
# =====================================================


@login_required
def reports_dashboard(request):


    total_events = Event.objects.count()


    total_users = User.objects.count()


    total_registrations = Registration.objects.count()






    monthly_registrations = []


    months = []



    for month in range(1,13):


        months.append(str(month))


        monthly_registrations.append(

            Registration.objects.filter(

                registration_date__month=month

            ).count()

        )







    context = {
    "total_events": total_events,
    "total_users": total_users,
    "total_registrations": total_registrations,
    "months": json.dumps(months),
    "monthly_registrations": json.dumps(monthly_registrations),
}

    if request.user.is_superuser or request.user.role == User.Role.ADMIN:
       context.update(get_admin_dashboard_context())

    elif request.user.role == User.Role.ORGANIZER:
       context.update(get_organizer_dashboard_context(request))

    else:
       context.update(get_attendee_dashboard_context(request))



    return render(

        request,

        "dashboard/reports.html",

        context

    )

    # =====================================================
# EXPORT EVENTS CSV
# =====================================================


@login_required
def export_events_csv(request):


    response = HttpResponse(
        content_type="text/csv"
    )


    response["Content-Disposition"] = (
        "attachment; filename=events.csv"
    )



    writer = csv.writer(response)



    writer.writerow([

        "Title",
        "Organizer",
        "Category",
        "Date",
        "Venue",
        "Status"

    ])




    events = Event.objects.select_related(
        "organizer",
        "category"
    )




    for event in events:


        writer.writerow([


            event.title,


            event.organizer.username,


            event.category.name,


            event.event_date,


            event.venue,


            event.status


        ])





    return response

# =====================================================
# EXPORT REGISTRATIONS CSV
# =====================================================


@login_required
def export_registrations_csv(request):


    response = HttpResponse(
        content_type="text/csv"
    )



    response["Content-Disposition"] = (
        "attachment; filename=registrations.csv"
    )




    writer = csv.writer(response)



    writer.writerow([


        "Attendee",
        "Event",
        "Registration Date",
        "Status",
        "Ticket Code"


    ])






    registrations = Registration.objects.select_related(
        "attendee",
        "event"
    )





    for registration in registrations:


        writer.writerow([


            registration.attendee.username,


            registration.event.title,


            registration.registration_date,


            registration.status,


            registration.ticket_code


        ])




    return response

    # =====================================================
# EXPORT USERS CSV
# =====================================================


@login_required
def export_users_csv(request):


    response = HttpResponse(
        content_type="text/csv"
    )



    response["Content-Disposition"] = (
        "attachment; filename=users.csv"
    )



    writer = csv.writer(response)



    writer.writerow([


        "Username",
        "Email",
        "Role",
        "Joined Date"


    ])





    users = User.objects.only(
    "id",
    "username",
    "first_name",
    "last_name",
    "email",
    "role",
)





    for user in users:


        writer.writerow([


            user.username,


            user.email,


            user.role,


            user.date_joined


        ])




    return response


# =====================================================
# CALENDAR VIEW
# =====================================================


@login_required
def calendar_view(request):


    events = Event.objects.filter(

        event_date__gte=timezone.localdate()

    ).values(

        "title",
        "event_date",
        "venue"

    )





    calendar_events = []




    for event in events:


        calendar_events.append({


            "title":
                event["title"],


            "start":
                str(event["event_date"]),


            "description":
                event["venue"]


        })







    context = {
    "calendar_events": json.dumps(calendar_events),
    "calendar_total": len(calendar_events),
}

    if request.user.is_superuser or request.user.role == User.Role.ADMIN:
        context.update(get_admin_dashboard_context())

    elif request.user.role == User.Role.ORGANIZER:
        context.update(get_organizer_dashboard_context(request))

    else:
        context.update(get_attendee_dashboard_context(request))

    return render(
        request,
        "dashboard/calendar.html",
        context,
    )




 