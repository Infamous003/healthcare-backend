from .models import Patient, Doctor
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import (
    PatientCreateSerializer,
    PatientPublicSerializer,
    PatientUpdateSerializer,
    RegisterSerializer,

    DoctorSerializer,
    DoctorPublicSerializer,
    DoctorCreateSerializer,
    DoctorUpdateSerializer
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# ----- Patient endpoints -----

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def patients_list(request):
    if request.method == "GET":
        patients = Patient.objects.all()
        serializer = PatientPublicSerializer(patients, many=True)

        return Response(serializer.data, status=200)
    
    elif request.method == "POST":
        serializer = PatientCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def patient_detail(request, pk):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response({"msg": "Patient Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PatientPublicSerializer(patient)
        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        serializer = PatientUpdateSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        patient.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

# ----- Auth endpoints -----

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----- Doctor endpoints -----

@api_view(["GET", "POST"])
def doctors_list(request):
    if request.method == "GET":
        doctors = Doctor.objects.all()
        serializer = DoctorPublicSerializer(doctors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = DoctorCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def doctor_detail(request, pk):
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response({"msg": "Doctor Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DoctorPublicSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = DoctorUpdateSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
