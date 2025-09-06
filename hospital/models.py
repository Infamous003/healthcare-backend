from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
]

class Patient(models.Model):
    firstname = models.CharField(max_length=64, help_text="Enter the patient's first name")
    lastname = models.CharField(max_length=64, help_text="Enter the patient's last name")
    email = models.EmailField(max_length=128, unique=True, help_text="Enter the patient's email address")
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], help_text="Enter the patient's age")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text="Select the patient's gender")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('CARD', 'Cardiologist'),
        ('DERM', 'Dermatologist'),
        ('NEUR', 'Neurologist'),
        ('ORTH', 'Orthopedic'),
        ('PED', 'Pediatrician'),
        ('GEN', 'General Physician'),
    ]

    firstname = models.CharField(max_length=64, help_text="Enter the doctor's first name")
    lastname = models.CharField(max_length=64, help_text="Enter the doctor's last name")
    max_appointments_per_day = models.IntegerField(default=10, help_text="Max appointments a doctor can have per day")
    email = models.EmailField(max_length=128, unique=True, help_text="Enter the doctor's email address")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text="Select the doctor's gender")
    specialization = models.CharField(max_length=4, choices=SPECIALIZATION_CHOICES, help_text="Select the doctor's specialization")

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.specialization})"

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="doctor_mappings")
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, related_name="patient_mappings")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("patient", "doctor")
    
    def __str__(self):
        return f"{self.patient} -> {self.doctor} ({self.assigned_at.date()})"