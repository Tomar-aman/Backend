# accounts/serializers.py
from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role','password']
      
    def create(self, validated_data):
        # Since we want to handle gender, age, city, state, and profile_picture elsewhere or later,
        # we don't include them in the registration process here.
        user = User(
            username=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
        )
        # Set a default password or handle it separately if required.
        user.set_password(validated_data['password'])  # Uncomment if you have a password field
        user.save()
        return user
