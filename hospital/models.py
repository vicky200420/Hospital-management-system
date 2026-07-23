from django.db import models
from django.conf import settings


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    logo = models.ImageField(upload_to="hospital_logos/", blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"
    




class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "DOCTOR"}
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    specialization = models.CharField(max_length=100)

    qualification = models.CharField(max_length=200)

    experience = models.PositiveIntegerField(
        help_text="Experience in years"
    )

    consultation_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    phone = models.CharField(max_length=15)

    photo = models.ImageField(
        upload_to="doctor_photos/",
        blank=True,
        null=True
    )

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"
    
    
    
class Patient(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    BLOOD_GROUP_CHOICES = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "PATIENT"},
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES,
    )

    address = models.TextField()

    emergency_contact = models.CharField(
        max_length=15
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.get_full_name()