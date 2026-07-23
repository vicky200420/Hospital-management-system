from django.urls import path
from . import views

urlpatterns = [

    path(
    "book/<int:doctor_id>/",
    views.book_appointment,
    name="book_appointment",
),
    path(
    "my-appointments/",
    views.my_appointments,
    name="my_appointments"
),
path(
    "doctor-appointments/",
    views.doctor_appointments,
    name="doctor_appointments"
),
path(
    "update-status/<int:appointment_id>/<str:status>/",
    views.update_appointment_status,
    name="update_appointment_status",
),
path(
    "doctor-patients/",
    views.doctor_patients,
    name="doctor_patients"
),
path(
    "manage-time-slots/",
    views.manage_time_slots,
    name="manage_time_slots"
),
path(
    "delete-time-slot/<int:slot_id>/",
    views.delete_time_slot,
    name="delete_time_slot"
),
]