from datetime import date, timedelta
from django.core.exceptions import ValidationError
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
            f"{doctor.first_name} {doctor.last_name} "
            f"({doctor.specialization})",
        )

    def test_doctor_years_of_experience(self):
        doctor = self.doctor
        today = timezone.now().date()
        expected_years = (
            today.year
            - doctor.hire_date.year
            - (
                (today.month, today.day)
                < (doctor.hire_date.month, doctor.hire_date.day)
            )
        )
        self.assertEqual(doctor.years_of_experience, expected_years)

    def test_doctor_hire_date_cannot_be_in_future(self):
        doctor = Doctor(
            username="future.doctor",
            first_name="Future",
            last_name="Doctor",
            specialization="Urologist",
            hire_date=timezone.now().date() + timedelta(days=1),
        )
        with self.assertRaisesMessage(
            ValidationError, "Hire date cannot be in the future"
        ):
            doctor.full_clean()


class PatientModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Smith",
            birth_date=date(1995, 5, 15),
            phone_number="+380991234567",
        )

    def test_patient_str(self):
        patient = self.patient
        self.assertEqual(
            str(patient),
            f"{patient.first_name} {patient.last_name}"
        )

    def test_patient_should_get_absolute_url(self):
        patient = self.patient
        self.assertEqual(patient.get_absolute_url(), f"/patient/{patient.id}/")

    def test_patient_birth_date_cannot_be_in_future(self):
        patient = Patient(
            first_name="John",
            last_name="Smith",
            birth_date=timezone.now().date() + timedelta(days=1),
            phone_number="+38099567123",
        )
        with self.assertRaisesMessage(
            ValidationError, "Birth date cannot be in the future"
        ):
            patient.full_clean()

    def test_patient_age_cannot_be_more_than_90(self):
        patient = Patient(
            first_name="John",
            last_name="Smith",
            birth_date=date(1900, 1, 1),
            phone_number="+380501234567",
        )
        with self.assertRaisesMessage(
            ValidationError,
            "Patient age seems unrealistic"
        ):
            patient.full_clean()

    def test_patient_phone_number_must_have_valid_format(self):
        patient = Patient(
            first_name="John",
            last_name="Smith",
            birth_date=date(1995, 5, 15),
            phone_number="12345",
        )
        with self.assertRaises(ValidationError):
            patient.full_clean()


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
            phone_number="+380991234567",
        )

    def test_appointment_str(self):
        appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=timezone.now() + timedelta(days=1),
        )
        self.assertEqual(
            str(appointment),
            f"({appointment.appointment_date:%d.%m.%Y}) {appointment.patient}",
        )

    def test_appointment_date_cannot_be_in_past(self):
        appointment = Appointment(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=timezone.now() - timedelta(days=1),
        )
        with self.assertRaisesMessage(
            ValidationError, "Appointment date cannot be in the past"
        ):
            appointment.full_clean()

    def test_doctor_cannot_have_appointment_within_10_minutes(self):
        first_appointment_date = timezone.now() + timedelta(days=1)
        second_appointment_date = first_appointment_date + timedelta(minutes=5)
        Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=first_appointment_date,
        )
        second_appointment = Appointment(
            doctor=self.doctor,
            patient=Patient.objects.create(
                first_name="Anna",
                last_name="Doe",
                birth_date=date(1990, 1, 1),
                phone_number="+380501234567",
            ),
            appointment_date=second_appointment_date,
        )
        with self.assertRaisesMessage(
            ValidationError,
            "This doctor already has an appointment within 10 minutes"
        ):
            second_appointment.full_clean()

    def test_patient_cannot_have_appointment_within_10_minutes(self):
        first_appointment_date = timezone.now() + timedelta(days=1)
        second_appointment_date = first_appointment_date + timedelta(minutes=5)
        Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=first_appointment_date,
        )
        another_doctor = Doctor.objects.create_user(
            username="another.doctor",
            password="test_password",
            first_name="Anna",
            last_name="Doctor",
            specialization="Radiologist",
            hire_date=date(2020, 1, 1),
        )
        second_appointment = Appointment(
            doctor=another_doctor,
            patient=self.patient,
            appointment_date=second_appointment_date,
        )
        with self.assertRaisesMessage(
            ValidationError,
            "This patient already has an appointment within 10 minutes"
        ):
            second_appointment.full_clean()


class CTScanModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            birth_date=date(1995, 5, 15),
            phone_number="+380991234567",
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

    def test_scan_cannot_be_in_future(self):
        ct_scan = CTScan(
            patient=self.patient,
            image="ct_scan/test.jpg",
            scan_date=timezone.now() + timedelta(days=1),
        )
        with self.assertRaisesMessage(
            ValidationError, "Scan date cannot be in the future"
        ):
            ct_scan.full_clean()

    def test_scan_cannot_be_before_patient_birth_date(self):
        ct_scan = CTScan(
            patient=self.patient,
            image="ct_scan/test.jpg",
            scan_date=self.patient.birth_date - timedelta(days=1),
        )
        with self.assertRaisesMessage(
            ValidationError,
            "Scan date cannot be earlier than patient's birth date"
        ):
            ct_scan.full_clean()

    def test_scan_cannot_have_duplicates(self):
        scan_date = timezone.now()
        CTScan.objects.create(
            patient=self.patient,
            image="ct_scan/test1.jpg",
            scan_date=scan_date
        )
        duplicate_ct_scan = CTScan(
            patient=self.patient,
            image="ct_scan/test2.jpg",
            scan_date=scan_date
        )

        with self.assertRaisesMessage(
            ValidationError,
            "This scan already exists"
        ):
            duplicate_ct_scan.full_clean()
