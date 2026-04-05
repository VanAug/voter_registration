from rest_framework import serializers
from .models import Applicant, RegistrationChannel

class ApplicantSerializer(serializers.ModelSerializer):
    registration_channel = serializers.ChoiceField(choices=RegistrationChannel.choices, required=False)

    class Meta:
        model = Applicant
        fields = ['id', 'full_name', 'phone_number', 'id_number', 'county', 
                  'voter_status', 'registration_channel', 'registered_at']
        read_only_fields = ['id', 'registered_at']

    def validate_phone_number(self, value):
        # Normalize Kenyan phone numbers to +254XXXXXXXXX format
        if value.startswith('0'):
            value = '+254' + value[1:]      # 0712345678 -> +254712345678
        elif value.startswith('254') and not value.startswith('+'):
            value = '+' + value              # 254712345678 -> +254712345678
        # Optionally, if number already starts with +254, leave as is
        
        # Now validate (your model's regex will also run, but we validate early)
        if not value.startswith('+254') or len(value) != 13:
            raise serializers.ValidationError(
                "Phone number must be a valid Kenyan number (e.g., 0712345678, +254712345678, 254712345678)"
            )
        return value

    def validate_id_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("ID Number must contain only digits")
        if len(value) < 5 or len(value) > 8:
            raise serializers.ValidationError("ID Number must be between 5 and 8 digits")
        return value