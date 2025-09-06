from django.test import TestCase

from rest_framework.test import APITestCase
from .models import Patient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class AuthTests(APITestCase):
    def setUp(self):
        # we creatin a user in the setup
        self.user = User.objects.create_user(
            username="defaultuser",
            email="default@gmail.com",
            password="password123"
        )
    def test_register_user(self):
        user_data = {
            "username": "testuser",
            "email": "testemail@gmail.com",
            "password": "testpassword"
        }
        response = self.client.post("/api/auth/register/", user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], user_data["username"])
    
    def test_login_success(self):
        login_data = {
            "username": "defaultuser",
            "password": "password123"
        }
        response = self.client.post("/api/auth/login/", login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        # Deliberately sending wrong login info
        response = self.client.post("/api/auth/login/", {"username": "wrong", "password": "wrong123"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

class PatientTests(APITestCase):
    # creating and loggin in as a test user, since some of the routes require access token
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post("/api/auth/login/", {"username": "testuser", "password": "password123"})
        self.token = response.data["access"]

        # setting the auth header for each test
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.data = {
            "firstname": "Erling", 
            "lastname": "Haaland", 
            "age": 26, 
            "gender": "M", 
            "email": "earling@gmail.com"
        }
    
    def test_create_patient(self):
        response = self.client.post("/api/patients/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["firstname"], self.data["firstname"])
        self.assertEqual(response.data["lastname"], self.data["lastname"])
    
    def test_get_patients(self):
        response = self.client.get("/api/patients/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_patient_by_id(self):
        # creating a user
        response = self.client.post("/api/patients/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data["id"]

        # by default it will have the id of 1
        response = self.client.get(f"/api/patients/{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["firstname"], self.data["firstname"])
        self.assertEqual(response.data["lastname"], self.data["lastname"])
    
    def test_get_patient_by_id_notfound(self):
        # patient with id 999 will obviously not exist
        response = self.client.get("/api/patients/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_patient(self):
        response = self.client.post("/api/patients/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data["id"]

        response = self.client.delete(f"/api/patients/{id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_delete_patient_notfound(self):
        response = self.client.delete("/api/patients/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_update_patient_notfound(self):
        data = {
            "firstname": "updatedname"
        }
        response = self.client.put("/api/patients/999/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_patient(self):
        response = self.client.post("/api/patients/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data["id"]
        updated_data = {
            "firstname": "Kiliyan",
            "lastname": "Mbappe",
        }
        response = self.client.put(f"/api/patients/{id}/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["firstname"], "Kiliyan")
        self.assertEqual(response.data["lastname"], "Mbappe")
    

class DoctorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post("/api/auth/login/", {"username": "testuser", "password": "password123"})
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.doctor_data = {
            "firstname": "Syed",
            "lastname": "Mehdi",
            "specialization": "DERM",
            "email": "syed@gmail.com",
            "gender": "M"
        }

    def test_create_doctor(self):
        response = self.client.post("/api/doctors/", self.doctor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["firstname"], self.doctor_data["firstname"])
        self.assertEqual(response.data["lastname"], self.doctor_data["lastname"])

    def test_get_all_doctors(self):
        self.client.post("/api/doctors/", self.doctor_data)
        response = self.client.get("/api/doctors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_doctor_by_id(self):
        response = self.client.post("/api/doctors/", self.doctor_data)
        id = response.data["id"]

        response = self.client.get(f"/api/doctors/{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["firstname"], self.doctor_data["firstname"])
        self.assertEqual(response.data["lastname"], self.doctor_data["lastname"])
    
    def test_get_doctor_by_id_notfound(self):
        response = self.client.get("/api/doctors/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_doctor(self):
        response = self.client.post("/api/doctors/", self.doctor_data)
        doctor_id = response.data["id"]

        response = self.client.delete(f"/api/doctors/{doctor_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_doctor_notfound(self):
        response = self.client.delete("/api/doctors/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
