from django.contrib import admin
from .models import Appointment, TimeSlot


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "patient",
        "doctor",
        "appointment_date",
        "appointment_time",
        "status",
    )

    list_filter = (
        "status",
        "appointment_date",
        "hospital",
    )

    search_fields = (
        "patient__user__first_name",
        "doctor__user__first_name",
    )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("doctor", "day_of_week", "start_time", "end_time", "is_available")
    list_filter = ("day_of_week", "is_available", "doctor")
    search_fields = ("doctor__user__first_name",)