from django.contrib import admin
from .models import Patient, Invoice, UploadReport

# Register your models here
admin.site.register(Patient)
admin.site.register(Invoice)
admin.site.register(UploadReport)
