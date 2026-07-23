from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
     path(
        "hospitals/",
        views.hospital_list,
        name="hospital_list"
    ),
     path(
    "hospital/<int:hospital_id>/",
    views.hospital_detail,
    name="hospital_detail",
    ),
    path(
    "doctor/<int:doctor_id>/",
    views.doctor_detail,
    name="doctor_detail"
    ),
    path(
    "patient-dashboard/",
    views.patient_dashboard,
    name="patient_dashboard",
),

path(
    "doctor-dashboard/",
    views.doctor_dashboard,
    name="doctor_dashboard",
),
path("about/", views.about, name="about"),
path("contact/", views.contact, name="contact"),
path("doctors/", views.doctor_list, name="doctor_list"),
path(
    "departments/",
    views.department_list,
    name="department_list"
),
path(
    "department/<int:department_id>/",
    views.department_detail,
    name="department_detail"
),
path(
    "patient-profile/",
    views.patient_profile,
    name="patient_profile"
),
path(
    "doctor-profile/",
    views.doctor_profile,
    name="doctor_profile"
),
]