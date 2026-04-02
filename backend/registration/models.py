from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class RegistrationChannel(models.TextChoices):
    USSD = 'USSD', 'USSD'
    WEBSITE = 'WEBSITE', 'Website'
    WHATSAPP = 'WHATSAPP', 'WhatsApp'

class Applicant(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\+?254[0-9]{9}$', 'Enter a valid Kenyan phone number.')]
    )
    id_number = models.CharField(max_length=20, unique=True)
    county = models.CharField(max_length=100)
    voter_status = models.BooleanField(default=False)
    registration_channel = models.CharField(
        max_length=20,
        choices=RegistrationChannel.choices,
        default=RegistrationChannel.WEBSITE
    )
    registered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['county']),
            models.Index(fields=['registration_channel']),
        ]
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"