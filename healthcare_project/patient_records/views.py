from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient, ContactDetails, MedicalHistory
from .serializers import PatientSerializer, ContactDetailsSerializer, MedicalHistorySerializer

class PatientListView(APIView):
    
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        print(request.query_params)
        name = request.query_params.get('name')
        dob = request.query_params.get('dob')
        patient_id = request.query_params.get('patient_id')

        queryset = Patient.objects.all()

        if name:
            queryset = queryset.filter(first_name__icontains=name) | queryset.filter(last_name__icontains=name)
        if dob:
            queryset = queryset.filter(dob=dob)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        serializer = PatientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientDetailView(APIView):
    
    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        contact_details = ContactDetails.objects.filter(patient=patient)
        medical_history = MedicalHistory.objects.filter(patient=patient)

        patient_serializer = PatientSerializer(patient)
        contact_serializer = ContactDetailsSerializer(contact_details, many=True)
        medical_history_serializer = MedicalHistorySerializer(medical_history, many=True)

        response_data = {
            "patient": patient_serializer.data,
            "contact_details": contact_serializer.data,
            "medical_history": medical_history_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
