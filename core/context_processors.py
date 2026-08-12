def dashboard_context(request):
    if not request.user.is_authenticated:
        return {}

    if request.user.is_superuser or request.user.role == "ADMIN":
        dashboard_type = "admin"
    elif request.user.role == "ORGANIZER":
        dashboard_type = "organizer"
    else:
        dashboard_type = "attendee"

    return {
        "dashboard_type": dashboard_type
    }