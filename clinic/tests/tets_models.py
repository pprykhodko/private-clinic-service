from datetime import date, timedelta
from django.utils import timezone
from django.test import TestCase

from clinic.models import Doctor, Patient, Appointment, CTScan


class DoctorModelTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            username="john.smith",
            password="test_password",
            first_name="John",
            last_name="Smith",
            specialization="Urologist",
            hire_date=date(2020, 1, 1),
        )

    def test_doctor_str(self):
        doctor = self.doctor
        self.assertEqual(
            str(doctor),
            f"{doctor.first_name} {doctor.last_name} ({doctor.specialization})"
        )

    def test_doctor_years_of_experience(self):
        doctor = self.doctor
        today = timezone.now().date()
        expected_years = (
            today.year - doctor.hire_date.year
            - (
                (today.month, today.day) <
                (doctor.hire_date.month, doctor.hire_date.day)
            )
        )
        self.assertEqual(
            doctor.years_of_experience, expected_years
        )


class PatientModelTest(TestCase):
    def test_patient_str(self):
        patient = Patient.objects.create(
            first_name="John",
            last_name="Smith",
            birth_date=date(1995, 5, 15),
            phone_number="+380991234567"
        )
        self.assertEqual(
            str(patient),
            f"{patient.first_name} {patient.last_name}"
        )


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            username="john.smith",
            password="test_password",
            first_name="John",
            last_name="Smith",
            specialization="Urologist",
            hire_date=date(2020, 1, 1),
        )

        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            birth_date=date(1995, 5, 15),
            phone_number="+380991234567"
        )

    def test_appointment_str(self):
        appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=timezone.now() + timedelta(days=1),
        )
        self.assertEqual(
            str(appointment),
            f"({appointment.appointment_date:%d.%m.%Y}) {appointment.patient}"
        )


class CTScanModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            birth_date=date(1995, 5, 15),
            phone_number="+380991234567"
        )

    def test_ct_scan_str(self):
        ct_scan = CTScan.objects.create(
            patient=self.patient,
            image="ct_scan/test.jpg",
            scan_date=date(2026, 5, 15)
        )
        self.assertEqual(
            str(ct_scan),
            f"CT Scan #{ct_scan.id} - {ct_scan.patient}"
        )
