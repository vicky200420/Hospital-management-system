from django.shortcuts import render,get_object_or_404
from .models import Hospital,Doctor
from django.contrib.auth.decorators import login_required
from .models import Doctor
from .models import Department
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, "hospital/home.html")

def hospital_list(request):

    hospitals = Hospital.objects.all()

    context = {
        "hospitals": hospitals
    }

    return render(
        request,
        "hospital/hospital_list.html",
        context
    )
    
def hospital_detail(request, hospital_id):

    hospital = get_object_or_404(Hospital, id=hospital_id)

    departments = hospital.departments.all()

    context = {
        "hospital": hospital,
        "departments": departments,
    }

    return render(
        request,
        "hospital/hospital_detail.html",
        context,
    )
    
def doctor_detail(request, doctor_id):

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    context = {
        "doctor": doctor
    }

    return render(
        request,
        "hospital/doctor_detail.html",
        context
    )
    

@login_required
def patient_dashboard(request):
    return render(request, "hospital/patient_dashboard.html")


@login_required
def doctor_dashboard(request):
    return render(request, "hospital/doctor_dashboard.html")

def about(request):
    return render(request, "hospital/about.html")


def contact(request):
    return render(request, "hospital/contact.html")

def doctor_list(request):

    doctors = Doctor.objects.filter(
        available=True
    )

    return render(
        request,
        "hospital/doctor_list.html",
        {
            "doctors": doctors
        }
    )
    
def department_list(request):

    departments = Department.objects.all()

    return render(
        request,
        "hospital/department_list.html",
        {
            "departments": departments
        }
    )
    
def department_detail(request, department_id):

    department = get_object_or_404(
        Department,
        id=department_id
    )

    doctors = department.doctors.all()

    context = {
        "department": department,
        "doctors": doctors,
    }

    return render(
        request,
        "hospital/department_detail.html",
        context
    )
    
@login_required
def patient_profile(request):
    return render(request, "hospital/patient_profile.html")


@login_required
def doctor_profile(request):
    return render(request, "hospital/doctor_profile.html")