from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms

from clinic.models import Patient, Appointment


class PatientForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        )
    )

    class Meta:
        model = Patient
        fields ="__all__"

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]

        today = timezone.now().date()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )

        if birth_date > timezone.now().date():
            raise ValidationError(
                "Birth date cannot be in the future."
            )

        if age > 120:
            raise ValidationError(
                "Patient age seems unrealistic."
            )
        return birth_date


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local",
            },
        )
    )

    class Meta:
        model = Appointment
        fields = "__all__"
