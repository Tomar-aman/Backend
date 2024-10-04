# accounts/utils.py
import random
from .models import OTPVerification

def send_otp(phone_number):
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP

    # Save OTP in the database
    OTPVerification.objects.create(phone_number=phone_number, otp=otp)

    # Here, you would add logic to send the OTP via SMS
    print(f"OTP sent to {phone_number}: {otp}")

    return otp
