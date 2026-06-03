from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clinic.models import Doctor, Patient, Appointment, CTScan
from clinic.tests.constants import DOCTOR_DATA, PATIENT_DATA

INDEX_URL = reverse("clinic:index")
DOCTOR_URL = reverse("clinic:doctor-list")
PATIENT_URL = reverse("clinic:patient-list")
APPOINTMENT_URL = reverse("clinic:appointment-list")
CTSCAN_URL = reverse("clinic:ct-scan-list")


class PublicViewsTest(TestCase):
    def test_index_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(**DOCTOR_DATA)
        self.patient = Patient.objects.create(**PATIENT_DATA)

        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=timezone.now() + timedelta(days=1)
        )

        self.ct_scan = CTScan.objects.create(
            patient=self.patient,
            image="ct_scan/test.jpg",
            scan_date=timezone.now()
        )

        self.client.force_login(self.doctor)

    def test_retrieve_index(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/index.html")

    def test_retrieve_doctors(self):
        response = self.client.get(DOCTOR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/doctor_list.html")

    def test_retrieve_doctor_details(self):
        response = self.client.get(
            reverse(
                "clinic:doctor-detail",
                kwargs={"pk": self.doctor.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/doctor_detail.html")

    def test_retrieve_patients(self):
        response = self.client.get(PATIENT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/patient_list.html")

    def test_retrieve_patient_details(self):
        response = self.client.get(
            reverse(
                "clinic:patient-detail",
                kwargs={"pk": self.patient.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/patient_detail.html")

    def test_retrieve_appointments(self):
        response = self.client.get(APPOINTMENT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/appointment_list.html")

    def test_retrieve_appointment_details(self):
        response = self.client.get(
            reverse(
                "clinic:appointment-detail",
                kwargs={"pk": self.appointment.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/appointment_detail.html")

    def test_retrieve_ct_scan(self):
        response = self.client.get(CTSCAN_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/ct_scan_list.html")

    def test_retrieve_ct_scan_details(self):
        response = self.client.get(
            reverse(
                "clinic:ct-scan-detail",
                kwargs={"pk": self.ct_scan.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clinic/ct_scan_detail.html")
