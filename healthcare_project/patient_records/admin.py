from django.contrib import admin
from .models import Patient, ContactDetails, MedicalHistory

admin.site.register(Patient)
admin.site.register(ContactDetails)
admin.site.register(MedicalHistory)
