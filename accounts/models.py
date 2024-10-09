from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    DOCTOR = 'doctor'
    PATIENT = 'patient'
    
    ROLE_CHOICES = [
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    def is_doctor(self):
        return self.role == self.DOCTOR
    
    def is_patient(self):
        return self.role == self.PATIENT
    
    def __str__(self):
        return f"{self.first_name}"


from django.utils import timezone
import random

# OTP Verification model
class OTPVerification(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        # Check if OTP is valid for 5 minutes
        return self.created_at >= timezone.now() - timezone.timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone_number}"
    