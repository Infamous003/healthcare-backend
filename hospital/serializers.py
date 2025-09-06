from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping
from django.contrib.auth.models import User

# ----- Patient Serializers -----
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "firstname", "lastname", "email", "age", "gender", "created_by"]

class PatientPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "firstname", "lastname", "age", "gender", "created_by"]

class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["firstname", "lastname", "age", "gender", "email"]

class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["firstname", "lastname", "age", "email"]


# ----- User Serializers -----
class RegisterSerializer(serializers.ModelSerializer):
    # This makes sure that the passwords aren't read
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    # Overriding the default create method cause we don't want plain password to be stored in db
    # create_user hashs the password
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        return user


# ----- Doctor Serializers -----
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "firstname", "lastname", "specialization", "max_appointments_per_day", "email", "gender"]
    
class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["firstname", "lastname", "specialization", "email", "gender"]
    
class DoctorPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "firstname", "lastname", "specialization", "max_appointments_per_day", "gender"]

class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["firstname", "lastname", "specialization", "email"]


# ----- Mappings Serializers -----
class MappingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["patient", "doctor", "assigned_at"]

class MappingsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCreateSerializer
        fields = ["patient", "doctor"]

class MappingsDetailSerializer(serializers.ModelSerializer):
    patient = PatientPublicSerializer()
    doctor = DoctorPublicSerializer()

    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "assigned_at"]