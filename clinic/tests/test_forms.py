from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from clinic.forms import PatientForm


class PatientFormTest(TestCase):
    def test_birth_date_cannot_be_in_future(self):
        form_data = {
            "first_name": "John",
            "last_name": "Smith",
            "birth_date": timezone.now().date() + timedelta(days=1),
            "phone_number": "+380991234567",
        }

        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Birth date cannot be in the future.", form.errors["birth_date"])

    def test_patient_age_cannot_be_more_than_120(self):
        form_data = {
            "first_name": "John",
            "last_name": "Smith",
            "birth_date": timezone.now().date().replace(year=1800),
            "phone_number": "+380991234567",
        }
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Patient age seems unrealistic.", form.errors["birth_date"])