from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "firstname", "lastname", "email", "age", "gender"]

class PatientPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["firstname", "lastname", "age", "gender"]

class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["firstname", "lastname", "age", "gender", "email"]

class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["firstname", "lastname", "age", "email"]
