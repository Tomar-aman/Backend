from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import DoctorProfile ,HospitalClinic, HospitalImage, DoctorEducation, DoctorVerification
from .serializers import DoctorProfileSerializer,HospitalClinicSerializer, HospitalImageSerializer, DoctorEducationSerializer, DoctorVerificationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from accounts.models import User
class DoctorProfileView(APIView):
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        try:
            doctor_profile = DoctorProfile.objects.get(user=user)  # Get the doctor profile based on user
            serializer = DoctorProfileSerializer(doctor_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DoctorProfile.DoesNotExist:
            return Response({"error": "Doctor profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        data = request.data

        try:
            doctor_profile = DoctorProfile.objects.get(user=user)
            user_profile = User.objects.get(username=request.user.username) # Get the doctor profile based on user
        except DoctorProfile.DoesNotExist:
            return Response({"error": "Doctor profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Update Doctor Profile
        user_profile.first_name = data.get('first_name', user_profile.first_name)
        user_profile.last_name = data.get('last_name', user_profile.last_name)
        user_profile.save()
        doctor_profile.specialty = data.get('specialty', doctor_profile.specialty)
        doctor_profile.experience_years = data.get('experience_years', doctor_profile.experience_years)
        doctor_profile.token_limit = data.get('token_limit', doctor_profile.token_limit)
        doctor_profile.gender = data.get('gender', doctor_profile.gender)
        doctor_profile.age = data.get('age', doctor_profile.age)
        doctor_profile.city = data.get('city', doctor_profile.city)
        doctor_profile.state = data.get('state', doctor_profile.state)

        if 'profile_picture' in request.FILES:
            doctor_profile.profile_picture = request.FILES['profile_picture']

         # Update Education (Handle as a list)
        if 'education' in data:
            # Clear existing education records
            doctor_profile.education.all().delete()
            # Add new education records
            education_list = data.get('education', [])
            for edu in education_list:
                DoctorEducation.objects.create(dcotor_profile=doctor_profile, education=edu)

        
        doctor_profile.save()
        return Response({"message": "Doctor profile updated successfully"}, status=status.HTTP_200_OK)



# Upload Hospital Images
class UploadHospitalImagesView(APIView):
    """
    Upload multiple hospital/clinic images.
    """
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    def post(self, request, hospital_id):
        hospital = HospitalClinic.objects.get(id=hospital_id)
        images = request.FILES.getlist('images')  # Get the list of uploaded files
        image_instances = []

        for image in images:
            image_instance = HospitalImage(hospital_clinic=hospital, image=image)
            image_instances.append(image_instance)
        
        HospitalImage.objects.bulk_create(image_instances)
        return Response({"message": "Images uploaded successfully"}, status=status.HTTP_201_CREATED)


# Doctor Verification
class DoctorVerificationView(APIView):
    """
    Handle doctor verification by uploading license documents.
    """
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    def post(self, request):
        user = request.user
        doctor_profile = user.doctor_profile

        # Check if doctor is already verified
        if DoctorVerification.objects.filter(doctor=doctor_profile).exists():
            return Response({"error": "Doctor is already verified"}, status=status.HTTP_400_BAD_REQUEST)

        verification_data = {
            'doctor': doctor_profile,
            'license_number': request.data.get('license_number'),
            'license_document': request.FILES.get('license_document'),
        }

        doctor_verification = DoctorVerification.objects.create(**verification_data)
        return Response({"message": "Verification details uploaded successfully"}, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Get verification status for the current doctor.
        """
        user = request.user
        doctor_profile = user.doctor_profile

        try:
            verification = DoctorVerification.objects.get(doctor=doctor_profile)
            serializer = DoctorVerificationSerializer(verification)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DoctorVerification.DoesNotExist:
            return Response({"message": "Doctor is not verified"}, status=status.HTTP_404_NOT_FOUND)
