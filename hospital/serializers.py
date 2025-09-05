from rest_framework import serializers
from .models import Patient
from django.contrib.auth.models import User

# ----- Patient Serializers -----
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