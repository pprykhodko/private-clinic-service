from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms

from clinic.models import Patient, Appointment, CTScan


def validate_appointment(doctor, appointment_date, instance_pk=None):
    if doctor and appointment_date:
        time_conflict = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__gt=appointment_date - timedelta(minutes=10),
            appointment_date__lt=appointment_date + timedelta(minutes=10)
        ).exclude(pk=instance_pk)

        if time_conflict.exists():
            raise ValidationError(
                "This doctor already has an appointment within 10 minutes"
            )

    if appointment_date < timezone.now():
        raise ValidationError(
            "Appointment date cannot be in the past."
        )


class DoctorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username",
            }
        )
    )


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
        fields = "__all__"

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


class PatientSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by last name",
            }
        )
    )


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local",
            }
        )
    )

    class Meta:
        model = Appointment
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        validate_appointment(
            cleaned_data.get("doctor"),
            cleaned_data.get("appointment_date"),
            self.instance.pk
        )
        return cleaned_data


class AppointmentUpdateForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local",
            }
        )
    )

    class Meta:
        model = Appointment
        fields = ("appointment_date", "notes")

    def clean(self):
        cleaned_data = super().clean()
        validate_appointment(
            self.instance.doctor,
            cleaned_data.get("appointment_date"),
            self.instance.pk
        )
        return cleaned_data


class AppointmentSearchForm(forms.Form):
    patient = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by first or last name",
            }
        )
    )


class CTScanForm(forms.ModelForm):
    scan_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local",
            }
        )
    )

    class Meta:
        model = CTScan
        fields = "__all__"

    def clean_scan_date(self):
        scan_date = self.cleaned_data["scan_date"]

        if scan_date > timezone.now():
            raise ValidationError(
                "Scan date cannot be in the future."
            )
        return scan_date

    def clean(self):
        cleaned_data = super().clean()

        patient = cleaned_data.get("patient")
        scan_date = cleaned_data.get("scan_date")

        if patient and scan_date and scan_date.date() < patient.birth_date:
            raise ValidationError(
                "Scan date cannot be earlier than patient's birth date."
            )

        if CTScan.objects.filter(
            patient=patient, scan_date=scan_date
        ).exists():
            raise ValidationError(
                "This scan already exists."
            )
        return cleaned_data


class CTScanSearchForm(forms.Form):
    patient = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by first or last name",
            }
        )
    )
