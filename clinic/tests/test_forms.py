from datetime import timedelta, date
from django.test import TestCase
from django.utils import timezone

from clinic.forms import PatientForm, AppointmentForm, AppointmentUpdateForm
from clinic.models import Doctor, Patient


class PatientFormTest(TestCase):
    def test_patient_creation_form_with_valid_data(self):
        form_data = {
            "first_name": "John",
            "last_name": "Smith",
            "birth_date": "1995-05-15",
            "phone_number": "+380991234567",
            "diagnosis": "-",
        }
        form = PatientForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["first_name"], form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"], form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["phone_number"], form_data["phone_number"]
        )


class AppointmentFormTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            username="doctor",
            password="password123",
            first_name="John",
            last_name="Smith",
            specialization="Urologist",
            hire_date=date(2020, 1, 1),
        )
        self.patient = Patient.objects.create(
            first_name="Anna",
            last_name="Doe",
            birth_date=date(1995, 5, 15),
            phone_number="+380991234567",
        )

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
