from .models import Patient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientCreateSerializer, PatientPublicSerializer, PatientSerializer, PatientUpdateSerializer
from rest_framework import status

@api_view(["GET", "POST"])
def patients_list(request):
    if request.method == "GET":
        patients = Patient.objects.all()
        serializer = PatientPublicSerializer(patients, many=True)

        return Response(serializer.data, status=200)
    
    elif request.method == "POST":
        # if not request.user or not request.user.is_authenticated:
        #     return Response(
        #         {"detail": "Unauthorized access"},
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )
        
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
        serializer = PatientUpdateSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        patient.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)