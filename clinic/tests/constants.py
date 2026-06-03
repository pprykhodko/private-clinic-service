from datetime import date


DOCTOR_DATA = {
    "username": "john.smith",
    "password": "test_password",
    "first_name": "John",
    "last_name": "Smith",
    "specialization": "Urologist",
    "hire_date": date(2020, 1, 1),
}

PATIENT_DATA = {
    "first_name": "Jack",
    "last_name": "Doe",
    "birth_date": date(1995, 5, 15),
    "phone_number": "+380991234567",
    "diagnosis": "-",
}

ANOTHER_DOCTOR_DATA = {
    "username": "anna.brown",
    "password": "test_password",
    "first_name": "Anna",
    "last_name": "Brown",
    "specialization": "Radiologist",
    "hire_date": date(2020, 1, 1),
}

ANOTHER_PATIENT_DATA = {
    "first_name": "Anna",
    "last_name": "Doe",
    "birth_date": date(1990, 1, 1),
    "phone_number": "+380501234567",
    "diagnosis": "-",
}

PATIENT_FORM_DATA = {
    "first_name": "Jack",
    "last_name": "Doe",
    "birth_date": "1995-05-15",
    "phone_number": "+380991234567",
    "diagnosis": "-",
}
