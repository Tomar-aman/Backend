from django.db import models
from doctor.models import DoctorProfile
from patient.models import PatientProfile
# Create your models here.

class Token(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    token_number = models.IntegerField()
    is_served = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'token_number', 'created_at')

    def __str__(self):
        return f"Token {self.token_number} for {self.patient.user.first_name} (Doctor: {self.doctor.user.first_name})"

