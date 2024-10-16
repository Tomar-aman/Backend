# doctor/models.py
from django.db import models
from accounts.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)
    experience_years = models.IntegerField(blank=True,null=True)
    token_limit = models.IntegerField(blank=True,null=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=5,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='media/profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name}"
    
from django.db import models

class HospitalClinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    hospital_picture = models.ImageField(upload_to='media/hospital_pictures/', null=True, blank=True)

    def __str__(self):
        return self.name

class HospitalImage(models.Model):
    hospital_clinic = models.ForeignKey(HospitalClinic, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/hospital_images/')

    def __str__(self):
        return f"Image for {self.hospital_clinic.name}"
class DoctorEducation(models.Model):
    dcotor_profile = models.ForeignKey(DoctorProfile, related_name='education', on_delete=models.CASCADE)
    education = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return f"Image for {self.dcotor_profile.user.first_name}"

class DoctorVerification(models.Model):
    doctor = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE, related_name='verification')
    is_verified = models.BooleanField(default=False)
    license_number = models.CharField(max_length=100, unique=True)
    license_document = models.FileField(upload_to='media/doctor_licenses/')
    verified_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)

    def __str__(self):
        return f"Verification status for {self.doctor.user.first_name} {self.doctor.user.last_name}"
