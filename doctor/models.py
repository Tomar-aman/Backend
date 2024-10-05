# doctor/models.py
from django.db import models
from accounts.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic_name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    experience_years = models.IntegerField(blank=True,null=True)
    token_limit = models.IntegerField(blank=True,null=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=5,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name}"
    
