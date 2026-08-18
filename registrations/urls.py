from django.urls import path

from . import views


urlpatterns = [

    path(
        "events/<slug:slug>/register/",
        views.register_event,
        name="register_event",
    ),

    path(
        "my-registrations/",
        views.my_registrations,
        name="my_registrations",
    ),

    path(
        "my-registrations/<int:registration_id>/cancel/",
        views.cancel_registration,
        name="cancel_registration",
    ),

    # =========================================
    # EVENT QR CHECK-IN
    # =========================================

    path(
        "events/<slug:slug>/check-in/",
        views.qr_checkin,
        name="qr_checkin",
    ),

    path(
        "events/<slug:slug>/check-in/verify/",
        views.verify_qr_checkin,
        name="verify_qr_checkin",
    ),

    # =========================================
    # ATTENDEE TICKET
    # =========================================

    path(
        "my-registrations/<int:registration_id>/ticket/",
        views.ticket_detail,
        name="ticket_detail",
    ),

]