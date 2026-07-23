from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from hospital.models import Hospital, Department, Doctor, Patient
from appointments.models import Appointment
from accounts.models import User
from .forms import HospitalForm, DepartmentForm, DoctorUserForm, DoctorProfileForm, PatientUserForm, PatientProfileForm


@login_required
def admin_dashboard(request):
    context = {
        "hospital_count": Hospital.objects.count(),
        "department_count": Department.objects.count(),
        "doctor_count": Doctor.objects.count(),
        "patient_count": Patient.objects.count(),
        "appointment_count": Appointment.objects.count(),
        "pending_count": Appointment.objects.filter(status="Pending").count(),
        "recent_appointments": Appointment.objects.order_by("-created_at")[:5]
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related("patient__user", "doctor__user", "hospital", "department").order_by("-appointment_date")
    return render(request, "dashboard/appointment_list.html", {"appointments": appointments})


@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    return redirect("appointment_list")


# ===== HOSPITAL CRUD =====

@login_required
def hospital_list(request):
    hospitals = Hospital.objects.all().order_by("name")
    return render(request, "dashboard/hospital_list.html", {"hospitals": hospitals})


@login_required
def add_hospital(request):
    if request.method == "POST":
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hospital added successfully.")
            return redirect("admin_hospital_list")
    else:
        form = HospitalForm()
    return render(request, "dashboard/add_hospital.html", {"form": form, "editing": False})


@login_required
def edit_hospital(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    if request.method == "POST":
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            messages.success(request, "Hospital updated successfully.")
            return redirect("admin_hospital_list")
    else:
        form = HospitalForm(instance=hospital)
    return render(request, "dashboard/add_hospital.html", {"form": form, "editing": True})


@login_required
def delete_hospital(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    hospital.delete()
    messages.success(request, "Hospital deleted successfully.")
    return redirect("admin_hospital_list")


# ===== DEPARTMENT CRUD =====

@login_required
def department_list(request):
    departments = Department.objects.select_related("hospital").all().order_by("name")
    return render(request, "dashboard/department_list.html", {"departments": departments})


@login_required
def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully.")
            return redirect("admin_department_list")
    else:
        form = DepartmentForm()
    return render(request, "dashboard/add_department.html", {"form": form, "editing": False})


@login_required
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
            return redirect("admin_department_list")
    else:
        form = DepartmentForm(instance=department)
    return render(request, "dashboard/add_department.html", {"form": form, "editing": True})


@login_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, "Department deleted successfully.")
    return redirect("admin_department_list")


# ===== DOCTOR CRUD =====

@login_required
def doctor_list(request):
    doctors = Doctor.objects.select_related("user", "hospital", "department").all().order_by("user__first_name")
    return render(request, "dashboard/doctor_list.html", {"doctors": doctors})


@login_required
def add_doctor(request):
    if request.method == "POST":
        user_form = DoctorUserForm(request.POST)
        profile_form = DoctorProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = "DOCTOR"
            password = user_form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Doctor added successfully.")
            return redirect("admin_doctor_list")
    else:
        user_form = DoctorUserForm()
        profile_form = DoctorProfileForm()
    return render(request, "dashboard/add_doctor.html", {
        "user_form": user_form, "profile_form": profile_form, "editing": False
    })


@login_required
def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor.objects.select_related("user"), pk=pk)
    if request.method == "POST":
        user_form = DoctorUserForm(request.POST, instance=doctor.user)
        profile_form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            profile_form.save()
            messages.success(request, "Doctor updated successfully.")
            return redirect("admin_doctor_list")
    else:
        user_form = DoctorUserForm(instance=doctor.user)
        profile_form = DoctorProfileForm(instance=doctor)
    return render(request, "dashboard/add_doctor.html", {
        "user_form": user_form, "profile_form": profile_form, "editing": True
    })


@login_required
def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.user.delete()
    messages.success(request, "Doctor deleted successfully.")
    return redirect("admin_doctor_list")


# ===== PATIENT CRUD =====

@login_required
def patient_list(request):
    patients = Patient.objects.select_related("user").all().order_by("user__first_name")
    return render(request, "dashboard/patient_list.html", {"patients": patients})


@login_required
def add_patient(request):
    if request.method == "POST":
        user_form = PatientUserForm(request.POST)
        profile_form = PatientProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = "PATIENT"
            password = user_form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Patient added successfully.")
            return redirect("admin_patient_list")
    else:
        user_form = PatientUserForm()
        profile_form = PatientProfileForm()
    return render(request, "dashboard/add_patient.html", {
        "user_form": user_form, "profile_form": profile_form, "editing": False
    })


@login_required
def edit_patient(request, pk):
    patient = get_object_or_404(Patient.objects.select_related("user"), pk=pk)
    if request.method == "POST":
        user_form = PatientUserForm(request.POST, instance=patient.user)
        profile_form = PatientProfileForm(request.POST, instance=patient)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            profile_form.save()
            messages.success(request, "Patient updated successfully.")
            return redirect("admin_patient_list")
    else:
        user_form = PatientUserForm(instance=patient.user)
        profile_form = PatientProfileForm(instance=patient)
    return render(request, "dashboard/add_patient.html", {
        "user_form": user_form, "profile_form": profile_form, "editing": True
    })


@login_required
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.user.delete()
    messages.success(request, "Patient deleted successfully.")
    return redirect("admin_patient_list")


# ===== REPORTS =====

@login_required
def reports(request):
    context = {
        "hospital_count": Hospital.objects.count(),
        "department_count": Department.objects.count(),
        "doctor_count": Doctor.objects.count(),
        "patient_count": Patient.objects.count(),
        "appointment_count": Appointment.objects.count(),
        "pending_count": Appointment.objects.filter(status="Pending").count(),
        "approved_count": Appointment.objects.filter(status="Approved").count(),
        "completed_count": Appointment.objects.filter(status="Completed").count(),
        "cancelled_count": Appointment.objects.filter(status="Cancelled").count(),
    }
    return render(request, "dashboard/reports.html", context)
