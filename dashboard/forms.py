from django import forms
from hospital.models import Hospital, Department, Doctor, Patient
from accounts.models import User


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ["name", "address", "phone", "email", "description"]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["hospital", "name", "description"]


class DoctorUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["password"].required = False
            self.fields["password"].help_text = "Leave blank to keep current password"


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["hospital", "department", "specialization", "qualification", "experience", "consultation_fee", "phone", "photo", "available"]


class PatientUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["password"].required = False
            self.fields["password"].help_text = "Leave blank to keep current password"


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["date_of_birth", "gender", "blood_group", "address", "emergency_contact"]
