from .models import Patient, Doctor, PatientDoctorMapping
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import (
    PatientCreateSerializer,
    PatientPublicSerializer,
    PatientUpdateSerializer,
    RegisterSerializer,

    DoctorPublicSerializer,
    DoctorCreateSerializer,
    DoctorUpdateSerializer,

    MappingsSerializer,
    MappingsDetailSerializer
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# ----- Patient endpoints -----

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def patients_list(request):
    if request.method == "GET":
        # getting only the patients that are owned by the logged in user
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientPublicSerializer(patients, many=True)

        return Response(serializer.data, status=200)
    
    elif request.method == "POST":
        serializer = PatientCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
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
    

# ----- Mappings endpoints -----

@api_view(["GET", "POST"])
def mappings_list(request):
    if request.method == "GET":
        mappings = PatientDoctorMapping.objects.all()
        serializer = MappingsDetailSerializer(mappings, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = MappingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def mapping_detail(request, patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        return Response({"detail": "Patient Not Found"}, status=status.HTTP_404_NOT_FOUND)

    mappings = PatientDoctorMapping.objects.filter(patient=patient)

    if request.method == "GET":
        # basically gettin all the docs of the patient
        doctors = [mapping.doctor for mapping in mappings]

        # Serializing the docs
        serializer = DoctorPublicSerializer(doctors, many=True)
        resp = {
            "patient": f"{patient.firstname} {patient.lastname}",
            "doctors": serializer.data
        }
        return Response(resp, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def mapping_delete(request, pk):
    try:
        mapping = PatientDoctorMapping.objects.get(pk=pk)
    except PatientDoctorMapping.DoesNotExist:
        return Response({"detail": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
    
    mapping.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)