from django.urls import path

from .views import (
    dashboard_home,
    reports_dashboard,
    export_events_csv,
    export_registrations_csv,
    export_users_csv,
    calendar_view,
)

urlpatterns = [
    path(
        "",
        dashboard_home,
        name="dashboard_home",
    ),

    # Calendar

    path(
        "calendar/",
        calendar_view,
        name="calendar_view",
    ),

    # Reports Dashboard

    path(
        "reports/",
        reports_dashboard,
        name="reports_dashboard",
    ),

    # CSV Exports

    path(
        "reports/events/",
        export_events_csv,
        name="export_events_csv",
    ),

    path(
        "reports/registrations/",
        export_registrations_csv,
        name="export_registrations_csv",
    ),

    path(
        "reports/users/",
        export_users_csv,
        name="export_users_csv",
    ),
]