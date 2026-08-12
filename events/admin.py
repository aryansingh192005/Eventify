from django.contrib import admin

from .models import Event, EventCategory


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_at",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "name",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "organizer",
        "event_date",
        "status",
        "available_seats",
        "is_featured",
    )

    list_filter = (
        "status",
        "category",
        "is_featured",
        "event_date",
    )

    search_fields = (
        "title",
        "venue",
        "description",
    )

    autocomplete_fields = (
        "organizer",
        "category",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-event_date",
    )