from django import forms

from clinic.models import Patient, Appointment, CTScan


class DoctorSearchForm(forms.Form):
    doctor = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by first or last name",
            }
        ),
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


class PatientSearchForm(forms.Form):
    patient = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by first or last name",
            }
        ),
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


class AppointmentSearchForm(PatientSearchForm):
    pass


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


class CTScanSearchForm(PatientSearchForm):
    pass
