from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

from registrations.models import Registration

from .services import (
    ask_gemini,
    get_navigation_links,
    detect_registration_request,
    find_event_from_message,
    detect_cancellation_request,
    find_user_registration_from_message,
    detect_ticket_request,
    find_user_ticket_from_message,
)


@login_required
@require_POST
def chat_api(request):

    message = request.POST.get(
        "message",
        "",
    ).strip()

    if not message:

        return JsonResponse(
            {
                "success": False,
                "reply": "Please enter a message.",
                "links": [],
            },
            status=400,
        )

    try:

        # ==================================================
        # 1. CANCELLATION REQUEST
        # ==================================================

        if detect_cancellation_request(message):

            registration = (
                find_user_registration_from_message(
                    message,
                    request.user,
                )
            )

            # ----------------------------------------------
            # Registration not found
            # ----------------------------------------------

            if not registration:

                event = find_event_from_message(
                    message
                )

                if event:

                    return JsonResponse(
                        {
                            "success": False,
                            "reply": (
                                f"You do not have an active "
                                f"registration for "
                                f"{event.title}."
                            ),
                            "links": [
                                {
                                    "label": "My Registrations",
                                    "url": reverse(
                                        "my_registrations"
                                    ),
                                }
                            ],
                        }
                    )

                return JsonResponse(
                    {
                        "success": True,
                        "reply": (
                            "I couldn't identify which "
                            "event registration you want "
                            "to cancel. Please mention "
                            "the event name."
                        ),
                        "links": [
                            {
                                "label": "My Registrations",
                                "url": reverse(
                                    "my_registrations"
                                ),
                            }
                        ],
                    }
                )

            # ----------------------------------------------
            # Already cancelled
            # ----------------------------------------------

            if (
                registration.status
                == Registration.Status.CANCELLED
            ):

                return JsonResponse(
                    {
                        "success": True,
                        "reply": (
                            f"Your registration for "
                            f"{registration.event.title} "
                            f"is already cancelled."
                        ),
                        "links": [
                            {
                                "label": "My Registrations",
                                "url": reverse(
                                    "my_registrations"
                                ),
                            }
                        ],
                    }
                )

            # ----------------------------------------------
            # Already attended
            # ----------------------------------------------

            if (
                registration.status
                == Registration.Status.ATTENDED
            ):

                return JsonResponse(
                    {
                        "success": False,
                        "reply": (
                            f"Your registration for "
                            f"{registration.event.title} "
                            f"cannot be cancelled because "
                            f"you have already attended "
                            f"the event."
                        ),
                        "links": [
                            {
                                "label": "My Registrations",
                                "url": reverse(
                                    "my_registrations"
                                ),
                            }
                        ],
                    }
                )

            # ----------------------------------------------
            # CONFIRMATION REQUIRED
            # ----------------------------------------------

            return JsonResponse(
                {
                    "success": True,
                    "reply": (
                        f"Are you sure you want to cancel "
                        f"your registration for "
                        f"{registration.event.title}?"
                    ),
                    "links": [
                        {
                            "label": "Yes, Cancel Registration",
                            "url": "#",
                            "action": "confirm_cancel",
                            "registration_id": registration.id,
                            "event_title": registration.event.title,
                        },
                        {
                            "label": "No, Keep Registration",
                            "url": "#",
                            "action": "cancel_confirmation",
                        },
                    ],
                }
            )

                # ==================================================
        # 2. TICKET / QR REQUEST
        # ==================================================

        if detect_ticket_request(message):

            registration = (
                find_user_ticket_from_message(
                    message,
                    request.user,
                )
            )


            # ----------------------------------------------
            # Event/ticket not found
            # ----------------------------------------------

            if not registration:

                event = find_event_from_message(
                    message
                )

                if event:

                    return JsonResponse(
                        {
                            "success": True,
                            "reply": (
                                f"I couldn't find an active "
                                f"ticket for {event.title}."
                            ),
                            "links": [
                                {
                                    "label": "My Registrations",
                                    "url": reverse(
                                        "my_registrations"
                                    ),
                                }
                            ],
                        }
                    )


                return JsonResponse(
                    {
                        "success": True,
                        "reply": (
                            "Please mention the event "
                            "name whose ticket you want "
                            "to view."
                        ),
                        "links": [
                            {
                                "label": "My Registrations",
                                "url": reverse(
                                    "my_registrations"
                                ),
                            }
                        ],
                    }
                )


            # ----------------------------------------------
            # Ticket found
            # ----------------------------------------------

            return JsonResponse(
    {
        "success": True,
        "reply": (
            f"Your ticket for "
            f"{registration.event.title} "
            f"is ready. 🎟️ "
            f"You can view your QR ticket below."
        ),
        "links": [
            {
                "label": (
                    f"View {registration.event.title} Ticket"
                ),
                "url": reverse(
                    "ticket_detail",
                    kwargs={
                        "registration_id":
                            registration.id,
                    },
                ),
            },
            {
                "label": "My Registrations",
                "url": reverse(
                    "my_registrations"
                ),
            },
        ],
    }
)
        # ==================================================
        # 2. REGISTRATION REQUEST
        # ==================================================

        if detect_registration_request(message):

            event = find_event_from_message(
                message
            )

            if event:

                registration = (
                    Registration.objects
                    .filter(
                        attendee=request.user,
                        event=event,
                    )
                    .first()
                )

                # ------------------------------------------
                # Already registered
                # ------------------------------------------

                if registration:

                    if (
                        registration.status
                        == Registration.Status.REGISTERED
                    ):

                        return JsonResponse(
                            {
                                "success": True,
                                "reply": (
                                    f"You are already "
                                    f"registered for "
                                    f"{event.title}. 🎟️"
                                ),
                                "links": [
                                    {
                                        "label": "My Registrations",
                                        "url": reverse(
                                            "my_registrations"
                                        ),
                                    }
                                ],
                            }
                        )

                # ------------------------------------------
                # Own event
                # ------------------------------------------

                if event.organizer == request.user:

                    return JsonResponse(
                        {
                            "success": False,
                            "reply": (
                                "You cannot register for "
                                "your own event."
                            ),
                            "links": [
                                {
                                    "label": (
                                        f"View {event.title}"
                                    ),
                                    "url": reverse(
                                        "event_detail",
                                        kwargs={
                                            "slug": event.slug,
                                        },
                                    ),
                                }
                            ],
                        }
                    )

                # ------------------------------------------
                # Registration closed
                # ------------------------------------------

                if not event.is_registration_open:

                    return JsonResponse(
                        {
                            "success": False,
                            "reply": (
                                f"Registration for "
                                f"{event.title} is "
                                f"currently closed."
                            ),
                            "links": [
                                {
                                    "label": (
                                        f"View {event.title}"
                                    ),
                                    "url": reverse(
                                        "event_detail",
                                        kwargs={
                                            "slug": event.slug,
                                        },
                                    ),
                                }
                            ],
                        }
                    )

                # ------------------------------------------
                # Registration available
                # ------------------------------------------

                return JsonResponse(
                    {
                        "success": True,
                        "reply": (
                            f"{event.title} is available "
                            f"for registration. "
                            f"Click below to register."
                        ),
                        "links": [
                            {
                                "label": (
                                    f"Register for "
                                    f"{event.title}"
                                ),
                                "url": reverse(
                                    "register_event",
                                    kwargs={
                                        "slug": event.slug,
                                    },
                                ),
                            }
                        ],
                    }
                )

        # ==================================================
        # 3. NORMAL AI CHAT
        # ==================================================

        reply = ask_gemini(
            message,
            request.user,
        )

        links = get_navigation_links(
            message,
            request.user,
        )

        return JsonResponse(
            {
                "success": True,
                "reply": reply,
                "links": links,
            }
        )

    except Exception as error:

        print(
            "Chatbot error:",
            error,
        )

        return JsonResponse(
            {
                "success": False,
                "reply": (
                    "I'm having trouble processing "
                    "your request right now. "
                    "Please try again."
                ),
                "links": [],
            },
            status=500,
        )