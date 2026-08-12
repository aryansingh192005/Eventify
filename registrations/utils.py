import qrcode

from io import BytesIO

from django.core.files import File


def generate_ticket_qr(registration):

    data = f"""
Ticket ID:
{registration.ticket_code}

Registration:
{registration.id}

Attendee:
{registration.attendee.username}

Event:
{registration.event.title}
"""


    qr = qrcode.make(data)


    buffer = BytesIO()

    qr.save(
        buffer,
        format="PNG"
    )


    filename = (
        f"ticket_{registration.ticket_code}.png"
    )


    registration.ticket_qr.save(
        filename,
        File(buffer),
        save=False,
    )


    registration.save(
        update_fields=[
            "ticket_qr"
        ]
    )

    return registration.ticket_qr