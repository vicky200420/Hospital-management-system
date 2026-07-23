from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class PatientRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "PATIENT"

        if commit:
            user.save()

        return user


class DoctorRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "DOCTOR"

        if commit:
            user.save()

        return user