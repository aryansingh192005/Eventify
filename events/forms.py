from datetime import datetime

from django import forms
from django.utils import timezone

from .models import Event, EventCategory


class EventCategoryForm(forms.ModelForm):

    class Meta:
        model = EventCategory

        fields = [
            "name",
            "description",
            "icon",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Category Name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Category Description",
                }
            ),

            "icon": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "bi-calendar-event",
                }
            ),
        }


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        exclude = [
            "organizer",
            "slug",
            "available_seats",
            "created_at",
            "updated_at",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Event Title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "venue": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Venue",
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "event_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "registration_deadline": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            "max_capacity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "is_featured": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    # ==========================================================
    # DATE / TIME VALIDATION
    # ==========================================================

    def clean(self):

        cleaned_data = super().clean()

        event_date = cleaned_data.get(
            "event_date"
        )

        start_time = cleaned_data.get(
            "start_time"
        )

        end_time = cleaned_data.get(
            "end_time"
        )

        registration_deadline = cleaned_data.get(
            "registration_deadline"
        )

        max_capacity = cleaned_data.get(
            "max_capacity"
        )

        price = cleaned_data.get(
            "price"
        )

        now = timezone.now()

        today = timezone.localdate()


        # ======================================================
        # 1. EVENT DATE REQUIRED
        # ======================================================

        if not event_date:

            return cleaned_data


        # ======================================================
        # 2. EVENT DATE CANNOT BE IN THE PAST
        # ======================================================

        if event_date < today:

            self.add_error(
                "event_date",
                "Event date cannot be in the past.",
            )


        # ======================================================
        # 3. START TIME REQUIRED
        # ======================================================

        if not start_time:

            return cleaned_data


        # ======================================================
        # 4. END TIME MUST BE AFTER START TIME
        # ======================================================

        if end_time:

            if end_time <= start_time:

                self.add_error(
                    "end_time",
                    "End time must be after the start time.",
                )


        # ======================================================
        # 5. BUILD EVENT START DATETIME
        # ======================================================

        event_start = None

        if event_date and start_time:

            event_start_naive = datetime.combine(
                event_date,
                start_time,
            )

            event_start = timezone.make_aware(
                event_start_naive,
                timezone.get_current_timezone(),
            )


        # ======================================================
        # 6. EVENT START CANNOT BE IN THE PAST
        # ======================================================

        if event_start:

            if event_start <= now:

                self.add_error(
                    "start_time",
                    "Event start time must be in the future.",
                )


        # ======================================================
        # 7. EVENT END MUST ALSO BE IN THE FUTURE
        # ======================================================

        if event_date and end_time:

            event_end_naive = datetime.combine(
                event_date,
                end_time,
            )

            event_end = timezone.make_aware(
                event_end_naive,
                timezone.get_current_timezone(),
            )

            if event_end <= now:

                self.add_error(
                    "end_time",
                    "Event end time must be in the future.",
                )


        # ======================================================
        # 8. REGISTRATION DEADLINE REQUIRED
        # ======================================================

        if not registration_deadline:

            return cleaned_data


        # ======================================================
        # 9. REGISTRATION DEADLINE CANNOT BE IN THE PAST
        # ======================================================

        if registration_deadline <= now:

            self.add_error(
                "registration_deadline",
                "Registration deadline must be in the future.",
            )


        # ======================================================
        # 10. DEADLINE MUST BE BEFORE EVENT START
        # ======================================================

        if event_start:

            if registration_deadline >= event_start:

                self.add_error(
                    "registration_deadline",
                    "Registration deadline must be before the event starts.",
                )


        # ======================================================
        # 11. DEADLINE MUST BE BEFORE EVENT DATE
        # ======================================================

        if event_date:

            deadline_local_date = timezone.localtime(
                registration_deadline
            ).date()

            if deadline_local_date > event_date:

                self.add_error(
                    "registration_deadline",
                    "Registration deadline must be before the event date.",
                )


        # ======================================================
        # 12. CAPACITY
        # ======================================================

        if max_capacity is not None:

            if max_capacity <= 0:

                self.add_error(
                    "max_capacity",
                    "Maximum capacity must be greater than zero.",
                )


        # ======================================================
        # 13. PRICE
        # ======================================================

        if price is not None:

            if price < 0:

                self.add_error(
                    "price",
                    "Event price cannot be negative.",
                )


        return cleaned_data