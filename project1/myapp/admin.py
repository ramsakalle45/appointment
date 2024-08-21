from django.contrib import admin
from .models import Patient, Invoice, UploadReport, CustomUser

# Register your models here
admin.site.register(Patient)
admin.site.register(Invoice)
admin.site.register(UploadReport)
admin.site.register(CustomUser)
