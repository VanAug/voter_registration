from django.contrib import admin
from .models import Applicant

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'id_number', 'county', 'voter_status', 'registration_channel', 'registered_at')
    list_filter = ('registration_channel', 'county', 'voter_status')
    search_fields = ('full_name', 'phone_number', 'id_number')