from django.shortcuts import render, redirect
from .forms import (PatientRegistrationForm, DoctorRegistrationForm,)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from accounts.models import User
from hospital.models import Patient
from hospital.models import Doctor, Hospital, Department


def patient_register(request):

    if request.method == "POST":

        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        date_of_birth = request.POST["date_of_birth"]
        gender = request.POST["gender"]
        blood_group = request.POST["blood_group"]
        address = request.POST["address"]
        emergency_contact = request.POST["emergency_contact"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:

            messages.error(request, "Passwords do not match")

            return redirect("patient_register")

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists")

            return redirect("patient_register")

        if User.objects.filter(email=email).exists():

            messages.error(request, "Email already exists")

            return redirect("patient_register")

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password1,
            role="PATIENT"
        )

        Patient.objects.create(
            user=user,
            date_of_birth=date_of_birth,
            gender=gender,
            blood_group=blood_group,
            address=address,
            emergency_contact=emergency_contact,
        )

        messages.success(
            request,
            "Registration successful. Please login."
        )

        return redirect("login")

    return render(
        request,
        "accounts/patient_register.html"
    )


def doctor_register(request):

    hospitals = Hospital.objects.all()
    departments = Department.objects.all()

    if request.method == "POST":

        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone = request.POST["phone"]

        hospital_id = request.POST["hospital"]
        department_id = request.POST["department"]

        specialization = request.POST["specialization"]
        qualification = request.POST["qualification"]
        experience = request.POST["experience"]
        consultation_fee = request.POST["consultation_fee"]

        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        photo = request.FILES.get("photo")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("doctor_register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("doctor_register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("doctor_register")

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password1,
            role="DOCTOR"
        )

        hospital = Hospital.objects.get(id=hospital_id)
        department = Department.objects.get(id=department_id)

        Doctor.objects.create(
            user=user,
            hospital=hospital,
            department=department,
            specialization=specialization,
            qualification=qualification,
            experience=experience,
            consultation_fee=consultation_fee,
            phone=phone,
            photo=photo
        )

        messages.success(
            request,
            "Doctor registered successfully. Please login."
        )

        return redirect("login")

    context = {
        "hospitals": hospitals,
        "departments": departments
    }

    return render(
        request,
        "accounts/doctor_register.html",
        context
    )


@ensure_csrf_cookie
def user_login(request):
    print("Request method:", request.method)
    print("POST data:", request.POST)

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == "ADMIN":
                return redirect("admin_dashboard")

            elif user.role == "DOCTOR":
                return redirect("doctor_dashboard")

            elif user.role == "PATIENT":
                return redirect("patient_dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


