from django.contrib import admin
from .models import Patient, Pharmacist, Medication, PatientNote

# DB 등록
admin.site.register(Patient)
admin.site.register(Pharmacist)
admin.site.register(Medication)
admin.site.register(PatientNote)