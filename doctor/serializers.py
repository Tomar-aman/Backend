from rest_framework import serializers
from .models import DoctorProfile, HospitalClinic, HospitalImage, DoctorEducation, DoctorVerification
from accounts.models import User 

# Serializer for Doctor's Education
class DoctorEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorEducation
        fields = ['education']


# Serializer for Hospital Images
class HospitalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalImage
        fields = ['id', 'image']


# Serializer for Hospital/Clinic
class HospitalClinicSerializer(serializers.ModelSerializer):
    images = HospitalImageSerializer(many=True, read_only=True)

    class Meta:
        model = HospitalClinic
        fields = ['id', 'name', 'address', 'city', 'state', 'phone_number', 'hospital_picture', 'images']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # user = serializers.StringRelatedField()  # This will return a string representation of the user
    education = DoctorEducationSerializer(many=True, required=False)
    # first_name = serializers.CharField(source='user.first_name', read_only=True)
    # last_name = serializers.CharField(source='user.last_name', read_only=True)
    # clinics = HospitalClinicSerializer(many=True, required=False)

    class Meta:
        model = DoctorProfile
        fields = ['user','specialty', 'experience_years', 'token_limit', 'gender', 'age', 'city', 'state', 'profile_picture', 'education']


# Serializer for Doctor Verification
class DoctorVerificationSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()

    class Meta:
        model = DoctorVerification
        fields = ['doctor', 'is_verified', 'license_number', 'license_document', 'verified_at']
