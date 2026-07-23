from django.urls import path
from . import views

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("appointments/", views.appointment_list, name="appointment_list"),
    path("appointments/<int:pk>/delete/", views.appointment_delete, name="appointment_delete"),

    # Hospitals
    path("hospitals/", views.hospital_list, name="admin_hospital_list"),
    path("hospital/add/", views.add_hospital, name="add_hospital"),
    path("hospital/<int:pk>/edit/", views.edit_hospital, name="edit_hospital"),
    path("hospital/<int:pk>/delete/", views.delete_hospital, name="delete_hospital"),

    # Departments
    path("departments/", views.department_list, name="admin_department_list"),
    path("department/add/", views.add_department, name="add_department"),
    path("department/<int:pk>/edit/", views.edit_department, name="edit_department"),
    path("department/<int:pk>/delete/", views.delete_department, name="delete_department"),

    # Doctors
    path("doctors/", views.doctor_list, name="admin_doctor_list"),
    path("doctor/add/", views.add_doctor, name="add_doctor"),
    path("doctor/<int:pk>/edit/", views.edit_doctor, name="edit_doctor"),
    path("doctor/<int:pk>/delete/", views.delete_doctor, name="delete_doctor"),

    # Patients
    path("patients/", views.patient_list, name="admin_patient_list"),
    path("patient/add/", views.add_patient, name="add_patient"),
    path("patient/<int:pk>/edit/", views.edit_patient, name="edit_patient"),
    path("patient/<int:pk>/delete/", views.delete_patient, name="delete_patient"),

    path("reports/", views.reports, name="reports"),
]
