from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Token
from doctor.models import DoctorProfile
from patient.models import PatientProfile
from django.shortcuts import get_object_or_404
from rest_framework import status

class BookAppointmentView(APIView):
    """
    Book an appointment with a doctor and assign a token number.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        doctor_id = request.data.get('doctor_id')
        patient_id = request.data.get('patient_id')

        # Get doctor and patient profiles
        doctor = get_object_or_404(DoctorProfile.objects.select_related('user'), user__username=doctor_id)
        patient = get_object_or_404(PatientProfile.objects.select_related('user'), user__username=patient_id)

        # Check if the patient has already booked an appointment with the doctor today
        today = datetime.date.today()
        existing_token = Token.objects.filter(doctor=doctor, patient=patient, created_at=today).first()

        if existing_token:
            return Response({
                "error": "You have already booked an appointment with this doctor for today."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the doctor's token limit is reached for the day
        token_count = Token.objects.filter(doctor=doctor, created_at=today).count()

        if token_count >= doctor.token_limit:
            return Response({
                "error": "The doctor's token limit for the day has been reached."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Assign the next available token number
        token_number = token_count + 1
        Token.objects.create(
            doctor=doctor,
            patient=patient,
            token_number=token_number,
            created_at=today  # This sets the appointment date as today
        )

        return Response({
            "message": f"Appointment booked successfully. Your token number is {token_number}"
        }, status=status.HTTP_201_CREATED)

class ViewTokensForToday(APIView):
    """
    Allows a doctor to view all patients with tokens for the current day.
    """
    def get(self, request):
        doctor_id = request.user.doctorprofile.id  # Assuming the doctor is authenticated
        today = datetime.date.today()
        
        # Get all tokens for the doctor for today
        tokens = Token.objects.filter(doctor_id=doctor_id, created_at=today).order_by('token_number')

        token_list = [
            {
                "patient_name": token.patient.user.get_full_name(),
                "token_number": token.token_number,
                "status": token.status,  # Waiting, In Progress, Served
                "created_at": token.created_at
            }
            for token in tokens
        ]

        return Response({"tokens": token_list}, status=status.HTTP_200_OK)

class UpdateTokenStatus(APIView):
    """
    Allows a doctor to update the status of a patient's token (e.g., mark as served).
    """
    def post(self, request):
        token_id = request.data.get('token_id')
        new_status = request.data.get('status')  # e.g., 'Served'

        try:
            token = Token.objects.get(id=token_id)
            token.is_served = True
            token.save()

            return Response({"message": "Token status updated successfully"}, status=status.HTTP_200_OK)

        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)
