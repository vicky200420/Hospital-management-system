from django.contrib import admin
from .models import Hospital, Department,Doctor,Patient


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hospital")
    list_filter = ("hospital",)
    search_fields = ("name",)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "hospital",
        "department",
        "specialization",
        "consultation_fee",
        "available",
    )

    list_filter = (
        "hospital",
        "department",
        "available",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "specialization",
    )
    


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "gender",
        "blood_group",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
    )