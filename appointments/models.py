from django.db import models
from hospital.models import Hospital, Department, Doctor, Patient


class TimeSlot(models.Model):
    DAYS_OF_WEEK = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="time_slots"
    )
    day_of_week = models.CharField(
        max_length=10,
        choices=DAYS_OF_WEEK
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["day_of_week", "start_time"]
        unique_together = ["doctor", "day_of_week", "start_time", "end_time"]

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week} {self.start_time}-{self.end_time}"


class Appointment(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.doctor.user.get_full_name()}"