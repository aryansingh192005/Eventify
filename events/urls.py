from django.urls import path

from . import views

urlpatterns = [

    # ==========================================================
    # HOME
    # ==========================================================

    path(
        "",
        views.home,
        name="home",
    ),

    # ==========================================================
    # CATEGORY MANAGEMENT
    # ==========================================================

    path(
        "categories/",
        views.category_list,
        name="category_list",
    ),

    path(
        "categories/create/",
        views.category_create,
        name="category_create",
    ),

    path(
        "categories/<int:pk>/edit/",
        views.category_update,
        name="category_update",
    ),

    path(
        "categories/<int:pk>/delete/",
        views.category_delete,
        name="category_delete",
    ),

    # ==========================================================
    # EVENT MANAGEMENT
    # ==========================================================

    path(
        "events/",
        views.event_list,
        name="event_list",
    ),

    path(
        "events/create/",
        views.event_create,
        name="event_create",
    ),

    path(
        "events/<slug:slug>/",
        views.event_detail,
        name="event_detail",
    ),

    path(
        "events/<slug:slug>/edit/",
        views.event_update,
        name="event_update",
    ),

    path(
        "events/<slug:slug>/delete/",
        views.event_delete,
        name="event_delete",
    ),

    # ==========================================================
    # ORGANIZER
    # ==========================================================

    path(
        "my-events/",
        views.my_events,
        name="my_events",
    ),

]