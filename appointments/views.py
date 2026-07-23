from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from hospital.models import Doctor
from .forms import AppointmentForm, TimeSlotForm
from .models import Appointment, TimeSlot
from hospital.models import Doctor, Patient
from django.contrib import messages
from django.shortcuts import redirect
from datetime import date

@login_required
@ensure_csrf_cookie
def book_appointment(request, doctor_id):

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(
            request,
            "Only patients can book appointments."
        )
        return redirect("home")

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            selected_date = form.cleaned_data["appointment_date"]
            selected_time = form.cleaned_data["appointment_time"]
            day_name = selected_date.strftime("%A")

            slot_exists = TimeSlot.objects.filter(
                doctor=doctor,
                day_of_week=day_name,
                start_time__lte=selected_time,
                end_time__gt=selected_time,
                is_available=True
            ).exists()

            already_booked = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=selected_date,
                appointment_time=selected_time,
                status__in=["Pending", "Approved"]
            ).exists()

            if not slot_exists:
                messages.error(
                    request,
                    f"The doctor is not available at {selected_time} on {day_name}. Please select an available time slot."
                )
            elif already_booked:
                messages.error(
                    request,
                    "This time slot is already booked. Please choose another time."
                )
            else:
                appointment = form.save(commit=False)

                appointment.hospital = doctor.hospital
                appointment.department = doctor.department
                appointment.doctor = doctor
                appointment.patient = patient
                appointment.status = "Pending"

                appointment.save()

                messages.success(
                    request,
                    "Appointment booked successfully."
                )

                return redirect("my_appointments")

    else:

        form = AppointmentForm()

    day_name = date.today().strftime("%A")
    available_slots = TimeSlot.objects.filter(
        doctor=doctor,
        is_available=True
    ).order_by("day_of_week", "start_time")

    return render(
        request,
        "appointments/book_appointment.html",
        {
            "doctor": doctor,
            "form": form,
            "available_slots": available_slots,
        }
    )
    
@login_required
def my_appointments(request):

    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(
            request,
            "Patient profile not found. Please contact support."
        )
        return redirect("patient_dashboard")

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-appointment_date", "-appointment_time")

    context = {
        "appointments": appointments
    }

    return render(
        request,
        "appointments/my_appointments.html",
        context
    )


@login_required
def doctor_appointments(request):

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by(
        "appointment_date",
        "appointment_time"
    )

    context = {
        "appointments": appointments
    }

    return render(
        request,
        "appointments/doctor_appointments.html",
        context
    )
    
    
@login_required
def update_appointment_status(request, appointment_id, status):

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if status in [
        "Approved",
        "Cancelled",
        "Completed"
    ]:

        appointment.status = status

        appointment.save()

    return redirect("doctor_appointments")

@login_required
def doctor_patients(request):

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related(
        "patient",
        "patient__user"
    ).order_by("-appointment_date")

    return render(
        request,
        "appointments/doctor_patients.html",
        {
            "appointments": appointments
        }
    )


@login_required
@ensure_csrf_cookie
def manage_time_slots(request):

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    if request.method == "POST":

        form = TimeSlotForm(request.POST)

        if form.is_valid():

            time_slot = form.save(commit=False)
            time_slot.doctor = doctor
            time_slot.save()

            messages.success(
                request,
                "Time slot added successfully."
            )

            return redirect("manage_time_slots")

    else:

        form = TimeSlotForm()

    time_slots = TimeSlot.objects.filter(
        doctor=doctor
    ).order_by("day_of_week", "start_time")

    return render(
        request,
        "appointments/manage_time_slots.html",
        {
            "form": form,
            "time_slots": time_slots,
        }
    )


@login_required
def delete_time_slot(request, slot_id):

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    time_slot = get_object_or_404(
        TimeSlot,
        id=slot_id,
        doctor=doctor
    )

    time_slot.delete()

    messages.success(
        request,
        "Time slot deleted successfully."
    )

    return redirect("manage_time_slots")