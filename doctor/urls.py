from django.urls import path
from .views import DoctorProfileView

urlpatterns = [
    path('doctor/profile/', DoctorProfileView.as_view(), name='doctor-profile'),
]
