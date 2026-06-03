from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from clinic.forms import PatientForm, AppointmentForm, AppointmentUpdateForm
from clinic.models import Doctor, Patient
from clinic.tests.constants import DOCTOR_DATA, PATIENT_DATA, PATIENT_FORM_DATA


class PatientFormTest(TestCase):
    def test_patient_creation_form_with_valid_data(self):
        form = PatientForm(data=PATIENT_FORM_DATA)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["first_name"],
            PATIENT_FORM_DATA["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            PATIENT_FORM_DATA["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["phone_number"],
            PATIENT_FORM_DATA["phone_number"]
        )


class AppointmentFormTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(**DOCTOR_DATA)
        self.patient = Patient.objects.create(**PATIENT_DATA)

    def test_appointment_creation_form_with_valid_data(self):
        form_data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "appointment_date": (
                timezone.now() + timedelta(days=1)
            ).strftime("%Y-%m-%dT%H:%M")
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_appointment_update_form_with_valid_fields(self):
        form = AppointmentUpdateForm()
        self.assertEqual(
            list(form.fields), ["appointment_date", "notes"]
        )
