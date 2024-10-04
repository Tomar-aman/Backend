from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User  # Your custom user model
from doctor.models import DoctorProfile # Import your doctor profile model
from patient.models import PatientProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_doctor_patient_profile(sender, instance, created, **kwargs):
    # Check if the user is a doctor and created a new user
    if created and instance.role == 'doctor':  # Assuming you have a 'role' field
        DoctorProfile.objects.create(user=instance)
    if created and instance.role == 'patient':  # Assuming you have a 'role' field
        PatientProfile.objects.create(user=instance)
