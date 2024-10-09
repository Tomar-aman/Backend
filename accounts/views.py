# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import User, OTPVerification
from .serializers import UserRegistrationSerializer
import random
from .utils import *


class SendOTPView(APIView):
    """
    Send OTP to the user's phone number after checking if it exists in the database.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        # Check if the phone number exists in the User model
        if  User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "Phone number is already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate and send OTP
        otp = send_otp(phone_number=phone_number)
        
        # Save OTP to the database or session (if necessary)
        request.session['verified_phone_number'] = phone_number
        
        # In a real-world app, send the OTP via SMS here (using Twilio or another service)
        return Response({"message": f"OTP sent to {phone_number}: {otp}"})  # Simulated OTP for now



class VerifyOTPView(APIView):
    """
    Verify the OTP sent to the user's phone number.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        print(phone_number)
        # Get the latest OTP for the phone number

        try:
            otp_record = OTPVerification.objects.filter(phone_number=phone_number).latest('created_at')
        except OTPVerification.DoesNotExist:
            return Response({"error": "OTP not found or expired"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the OTP is valid
        if otp_record.is_valid() and otp_record.otp == otp:
            otp_record.is_verified=True
            otp_record.save()
            return Response({"message": "OTP verified successfully"})
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    """
    Login using either email or phone number with password.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        number_email = request.data.get('number_email')
        # email = request.data.get('email')
        password = request.data.get('password')

        user = None
        
        if number_email:
            try:
                if '@' in number_email:  # Assume it's an email if it contains '@'
                    user = User.objects.get(email=number_email)
                else:
                    user = User.objects.get(phone_number=number_email)
            except User.DoesNotExist:
                return Response({"error": "User with these credentials does not exist"})
        
        if user and user.check_password(password):
            user = authenticate(username=user.phone_number, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,
                "message":"Login Successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """
    Registers a new user (Doctor or Patient) using the phone number from the session.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        # Retrieve the verified phone number from the session
        phone_number = request.session.get('verified_phone_number')

        if not phone_number:
            return Response({"error": "Phone number not verified. Please verify OTP first."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the phone number to the request data
        request.data['phone_number'] = phone_number

        # Proceed with registration
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "User registered successfully", "user": serializer.data,'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
