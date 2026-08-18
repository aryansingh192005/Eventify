from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from google import genai

from events.models import Event, EventCategory
from registrations.models import Registration


# ==========================================================
# GEMINI CLIENT
# ==========================================================

def get_gemini_client():

    if not settings.GEMINI_API_KEY:

        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.GEMINI_API_KEY
    )


# ==========================================================
# EVENTIFY DATABASE CONTEXT
# ==========================================================

def get_eventify_context(user):

    today = timezone.localdate()
    now = timezone.now()

    # ======================================================
    # PUBLISHED EVENTS
    # ======================================================

    events = (
        Event.objects
        .select_related(
            "category",
            "organizer",
        )
        .filter(
            status=Event.Status.PUBLISHED,
        )
        .order_by(
            "event_date",
            "start_time",
        )
    )

    event_lines = []

    for event in events:

        registration_open = (
            event.status == Event.Status.PUBLISHED
            and now <= event.registration_deadline
            and event.available_seats > 0
        )

        event_lines.append(
            f"""
Event:
- Title: {event.title}
- Category: {event.category.name}
- Description: {event.description}
- Venue: {event.venue}
- Date: {event.event_date}
- Start Time: {event.start_time}
- End Time: {event.end_time}
- Price: ₹{event.price}
- Maximum Capacity: {event.max_capacity}
- Available Seats: {event.available_seats}
- Registration Deadline: {event.registration_deadline}
- Registration Open: {"Yes" if registration_open else "No"}
- Featured: {"Yes" if event.is_featured else "No"}
- Organizer: {event.organizer.get_full_name() or event.organizer.username}
"""
        )

    if event_lines:

        events_context = "\n".join(
            event_lines
        )

    else:

        events_context = (
            "There are currently no published events."
        )

    # ======================================================
    # CATEGORIES
    # ======================================================

    categories = EventCategory.objects.all()

    category_lines = []

    for category in categories:

        category_lines.append(
            f"- {category.name}: "
            f"{category.description or 'No description available.'}"
        )

    if category_lines:

        categories_context = "\n".join(
            category_lines
        )

    else:

        categories_context = (
            "No event categories are currently available."
        )

    # ======================================================
    # CURRENT USER
    # ======================================================

    user_name = (
        user.get_full_name()
        or user.username
    )

    user_role = getattr(
        user,
        "role",
        "ATTENDEE",
    )

    # ======================================================
    # CURRENT USER REGISTRATIONS
    # ======================================================

    registrations = (
        Registration.objects
        .select_related(
            "event",
        )
        .filter(
            attendee=user,
        )
        .order_by(
            "-registration_date",
        )
    )

    registration_lines = []

    for registration in registrations:

        registration_lines.append(
            f"""
- Event: {registration.event.title}
  Status: {registration.get_status_display()}
  Registration Date: {registration.registration_date}
  Ticket ID: {registration.ticket_id()}
  Checked In: {"Yes" if registration.checked_in else "No"}
"""
        )

    if registration_lines:

        registrations_context = "\n".join(
            registration_lines
        )

    else:

        registrations_context = (
            "The user has no registrations."
        )

    # ======================================================
    # ORGANIZER EVENTS
    # ======================================================

    organizer_context = ""

    if user_role == "ORGANIZER":

        organizer_events = (
            Event.objects
            .filter(
                organizer=user,
            )
            .order_by(
                "event_date",
                "start_time",
            )
        )

        organizer_lines = []

        for event in organizer_events:

            registration_count = (
                Registration.objects
                .filter(
                    event=event,
                    status=Registration.Status.REGISTERED,
                )
                .count()
            )

            organizer_lines.append(
                f"""
- Event: {event.title}
  Status: {event.get_status_display()}
  Date: {event.event_date}
  Available Seats: {event.available_seats}
  Registered Attendees: {registration_count}
"""
            )

        if organizer_lines:

            organizer_context = "\n".join(
                organizer_lines
            )

        else:

            organizer_context = (
                "The organizer has not created any events."
            )

    # ======================================================
    # ADMIN SUMMARY
    # ======================================================

    admin_context = ""

    if user_role == "ADMIN":

        total_users = (
            user.__class__.objects.count()
        )

        total_events = Event.objects.count()

        total_registrations = (
            Registration.objects.count()
        )

        total_organizers = (
            user.__class__.objects
            .filter(
                role="ORGANIZER",
            )
            .count()
        )

        admin_context = f"""
Platform Summary:
- Total Users: {total_users}
- Total Organizers: {total_organizers}
- Total Events: {total_events}
- Total Registrations: {total_registrations}
"""

    # ======================================================
    # FINAL CONTEXT
    # ======================================================

    context = f"""
EVENTIFY PLATFORM CONTEXT

Current Date:
{today}

CURRENT USER

Name: {user_name}
Username: {user.username}
Role: {user_role}


PUBLISHED EVENTS

{events_context}


EVENT CATEGORIES

{categories_context}


CURRENT USER'S REGISTRATIONS

{registrations_context}


ORGANIZER INFORMATION

{organizer_context}


ADMIN INFORMATION

{admin_context}
"""

    return context


# ==========================================================
# GEMINI CHAT
# ==========================================================

def ask_gemini(
    message,
    user,
):

    client = get_gemini_client()

    eventify_context = get_eventify_context(
        user
    )

    system_instruction = """
You are the official Eventify Assistant.

Eventify is an event management platform.

Your job is to help users understand and use Eventify.

IMPORTANT RULES:

1. Use the Eventify context provided below when answering questions about Eventify.

2. Never invent event names, dates, prices, venues, organizers, seats, registrations, or other platform information.

3. If the requested information is not present in the context, clearly say that you do not have that information.

4. Respect the user's role.

5. Do not reveal private information about other users.

6. Do not expose ticket codes, registration details, or personal information belonging to another attendee.

7. You can explain how Eventify works.

8. Keep answers clear, concise, and helpful.

9. If the user asks about something unrelated to Eventify, you may answer normally.

10. You are an assistant, not an administrator. Do not claim that you performed an action unless the application actually performed it.

EVENTIFY CONTEXT:

"""

    prompt = (
        system_instruction
        + eventify_context
        + "\n\nUSER MESSAGE:\n"
        + message
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text


# ==========================================================
# NAVIGATION LINKS
# ==========================================================

def get_navigation_links(
    message,
    user,
):

    message_lower = message.lower()

    links = []

    # ======================================================
    # MY REGISTRATIONS
    # ======================================================

    registration_keywords = [
        "my registrations",
        "my registration",
        "registered events",
        "events i registered",
        "what am i registered",
        "my tickets",
        "my ticket",
    ]

    if any(
        keyword in message_lower
        for keyword in registration_keywords
    ):

        links.append(
            {
                "label": "My Registrations",
                "url": reverse(
                    "my_registrations"
                ),
            }
        )

    # ======================================================
    # PROFILE
    # ======================================================

    profile_keywords = [
        "my profile",
        "profile",
        "account",
        "edit profile",
    ]

    if any(
        keyword in message_lower
        for keyword in profile_keywords
    ):

        links.append(
            {
                "label": "My Profile",
                "url": reverse(
                    "profile"
                ),
            }
        )

    # ======================================================
    # DASHBOARD
    # ======================================================

    dashboard_keywords = [
        "dashboard",
        "my dashboard",
        "open dashboard",
    ]

    if any(
        keyword in message_lower
        for keyword in dashboard_keywords
    ):

        links.append(
            {
                "label": "Open Dashboard",
                "url": reverse(
                    "dashboard_home"
                ),
            }
        )

    # ======================================================
    # EVENT LIST
    # ======================================================

    event_list_keywords = [
        "all events",
        "browse events",
        "event list",
        "show events",
        "find events",
        "available events",
        "upcoming events",
    ]

    if any(
        keyword in message_lower
        for keyword in event_list_keywords
    ):

        links.append(
            {
                "label": "Browse Events",
                "url": reverse(
                    "event_list"
                ),
            }
        )

    # ======================================================
    # SPECIFIC EVENT
    # ======================================================

    events = Event.objects.filter(
        status=Event.Status.PUBLISHED
    )

    for event in events:

        event_title = event.title.lower()

        if event_title in message_lower:

            links.append(
                {
                    "label": f"View {event.title}",
                    "url": reverse(
                        "event_detail",
                        kwargs={
                            "slug": event.slug,
                        },
                    ),
                }
            )

            break

    # ======================================================
    # REMOVE DUPLICATES
    # ======================================================

    unique_links = []

    seen_urls = set()

    for link in links:

        if link["url"] not in seen_urls:

            unique_links.append(
                link
            )

            seen_urls.add(
                link["url"]
            )

    return unique_links


# ==========================================================
# REGISTRATION INTENT
# ==========================================================

def detect_registration_request(message):

    message_lower = message.lower()


    # ======================================================
    # CANCELLATION MUST ALWAYS WIN
    # ======================================================

    cancellation_words = [
        "cancel",
        "cancellation",
        "unregister",
        "withdraw",
        "remove my registration",
    ]

    if any(
        word in message_lower
        for word in cancellation_words
    ):

        return False


    # ======================================================
    # REGISTRATION PHRASES
    # ======================================================

    registration_phrases = [

        "register",
        "registration",
        "register me",

        "sign me up",
        "sign me in",

        "book me",
        "book my seat",

        "enroll me",
        "enrol me",

        "join the event",
        "join this event",

        "reserve my seat",
        "reserve a seat",

        "i want to attend",
        "i want to join",

    ]


    return any(
        phrase in message_lower
        for phrase in registration_phrases
    )


# ==========================================================
# FIND EVENT FROM MESSAGE
# ==========================================================

def find_event_from_message(message):

    message_lower = message.lower()

    events = Event.objects.filter(
        status=Event.Status.PUBLISHED
    )

    for event in events:

        if event.title.lower() in message_lower:

            return event

    return None


# ==========================================================
# CANCELLATION INTENT
# ==========================================================

def detect_cancellation_request(message):

    message_lower = message.lower()

    cancellation_phrases = [
        "cancel",
        "cancellation",
        "unregister",
        "withdraw",
        "remove my registration",
        "remove registration",
    ]

    return any(
        phrase in message_lower
        for phrase in cancellation_phrases
    )


# ==========================================================
# FIND USER'S REGISTRATION
# ==========================================================

def find_user_registration_from_message(
    message,
    user,
):

    event = find_event_from_message(
        message
    )

    if not event:

        return None

    return (
        Registration.objects
        .filter(
            attendee=user,
            event=event,
        )
        .first()
    )

# ==========================================================
# TICKET INTENT
# ==========================================================

def detect_ticket_request(message):

    message_lower = message.lower().strip()

    # ======================================================
    # EXPLICIT TICKET PHRASES
    # ======================================================

    ticket_phrases = [

        "show my ticket",
        "show me my ticket",
        "show ticket",

        "view my ticket",
        "view ticket",

        "my ticket",

        "ticket details",
        "ticket information",

        "ticket for",
        "ticket of",

        "show my qr",
        "show me my qr",

        "show my qr code",
        "show me my qr code",

        "view my qr",

        "my qr",
        "my qr code",

        "download my ticket",
        "download ticket",

    ]


    # ======================================================
    # DIRECT PHRASE MATCH
    # ======================================================

    if any(
        phrase in message_lower
        for phrase in ticket_phrases
    ):

        return True


    # ======================================================
    # NATURAL LANGUAGE MATCH
    # ======================================================

    has_ticket_word = (
        "ticket" in message_lower
        or "qr code" in message_lower
        or "qr" in message_lower
    )


    has_personal_reference = any(
        word in message_lower.split()
        for word in [
            "my",
            "mine",
            "me",
        ]
    )


    if (
        has_ticket_word
        and has_personal_reference
    ):

        return True


    return False

    message_lower = message.lower()

    ticket_phrases = [
        "show my ticket",
        "show ticket",
        "my ticket",
        "my qr",
        "show my qr",
        "qr code",
        "my qr code",
        "ticket for",
        "ticket of",
        "ticket details",
    ]

    return any(
        phrase in message_lower
        for phrase in ticket_phrases
    )

# ==========================================================
# FIND USER TICKET
# ==========================================================

def find_user_ticket_from_message(
    message,
    user,
):

    event = find_event_from_message(
        message
    )

    if not event:

        return None

    return (
        Registration.objects
        .filter(
            attendee=user,
            event=event,
        )
        .exclude(
            status=Registration.Status.CANCELLED
        )
        .first()
    )