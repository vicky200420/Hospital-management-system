from django import forms
from .models import Appointment, TimeSlot


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            "appointment_date",
            "appointment_time",
            "reason",
        ]

        widgets = {

            "appointment_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "appointment_time": forms.TimeInput(
                attrs={
                    "type": "time"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),

        }


class TimeSlotForm(forms.ModelForm):

    class Meta:
        model = TimeSlot
        fields = ["day_of_week", "start_time", "end_time", "is_available"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }