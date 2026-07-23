from django.urls import path
from . import views

urlpatterns = [

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "patient-register/",
        views.patient_register,
        name="patient_register"
    ),

    path(
        "doctor-register/",
        views.doctor_register,
        name="doctor_register"
    ),
    
]