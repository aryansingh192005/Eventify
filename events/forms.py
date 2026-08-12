from django import forms

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

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Event Title",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
            }),

            "category": forms.Select(attrs={
                "class": "form-select",
            }),

            "venue": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Venue",
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),

            "event_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "start_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time",
            }),

            "end_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time",
            }),

            "registration_deadline": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),

            "max_capacity": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),

            "status": forms.Select(attrs={
                "class": "form-select",
            }),

            "is_featured": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            if end_time <= start_time:
                self.add_error(
                    "end_time",
                    "End time must be after the start time."
                )

        return cleaned_data