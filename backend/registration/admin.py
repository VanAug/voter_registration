from django.contrib import admin
from django.http import HttpResponse
from .models import Applicant
import csv

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'id_number', 'county', 'voter_status', 'registration_channel', 'registered_at')
    list_filter = ('registration_channel', 'county', 'voter_status')
    search_fields = ('full_name', 'phone_number', 'id_number')
    readonly_fields = ('registered_at',)
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applicants.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Full Name', 'Phone', 'ID Number', 'County', 'Voter Status', 'Channel', 'Registered At'])
        for obj in queryset:
            writer.writerow([
                obj.id, obj.full_name, obj.phone_number, obj.id_number,
                obj.county, 'Yes' if obj.voter_status else 'No',
                obj.registration_channel, obj.registered_at
            ])
        return response
    export_as_csv.short_description = "Export selected to CSV"

admin.site.register(Applicant, ApplicantAdmin)