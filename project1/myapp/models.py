from django.db import models
from rest_framework import serializers
from django.utils.crypto import get_random_string


class Patient(models.Model):

    
    patient_name = models.CharField(max_length=200, null=True, blank=True)
    blood_group = models.CharField(max_length=200, null=True,blank=True)
    patient_age=models.IntegerField(null=True, blank=True)
    disease=models.CharField(max_length=100, null=True, blank=True)
    doctor_name=models.CharField(max_length=100, null=True, blank=True)
    mobile_number=models.IntegerField(null=True, blank=True)
    on_date=models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.disease}"
    
class Invoice(models.Model):
    patient= models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    patient_name = models.CharField(max_length=200, null=True,
   blank=True)
    blood_group = models.CharField(max_length=200, null=True,
   blank=True)
    patient_age=models.IntegerField(null=True, blank=True)
    disease=models.CharField(max_length=100, null=True, blank=True)
    doctor_name=models.CharField(max_length=100, null=True, blank=True)
    mobile_number=models.IntegerField(null=True, blank=True)
    on_date=models.DateField(null=True, blank=True)
    
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    invoice_date = models.DateField(auto_now_add=True)
    items = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
   
    def __str__(self):
        return f"Invoice #{self.invoice_number}"
    
class UploadReport(models.Model):
    patient_id=models.IntegerField(null=True, blank=True)
    report_name = models.CharField(max_length=200, null=True, blank=True)
    reports = models.FileField(null=True, upload_to='download_report/')  # Store the report file
    upload_date = models.DateTimeField(null=True, blank=True)  # Record upload date
    def __str__(self):
        return f"{self.report_name} - {self.patient_id}"

    # patient_id=models.CharField(null=True, blank=True, max_length=12)
    # reports=models.FileField(null=True, blank=True)
    # def __str__(self):
    #     return {self.patient_id}-{self.reports}
    


    




    
    
    

