from django.contrib import admin

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "attendee",
        "event",
        "status",
        "registration_date",
    )

    list_filter = (
        "status",
        "registration_date",
    )

    search_fields = (
        "attendee__username",
        "event__title",
    )

    autocomplete_fields = (
        "attendee",
        "event",
    )