from django.db import models
from rest_framework import serializers



class Patient(models.Model):

    patient_name = models.CharField(max_length=200, null=True,
   blank=True)
    blood_group = models.CharField(max_length=200, null=True,
   blank=True)
    patient_age=models.IntegerField(null=True, blank=True)
    disease=models.CharField(max_length=100, null=True, blank=True)
    doctor_name=models.CharField(max_length=100, null=True, blank=True)
    mobile_number=models.IntegerField(null=True, blank=True)
    on_date=models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"
    
class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    invoice_date = models.DateField(auto_now_add=True)
    patient_name = models.CharField(max_length=200) 
    blood_group = models.CharField(max_length=3) 
    patient_age = models.IntegerField()
    disease = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    on_date = models.DateField()
    items = models.TextField() 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Invoice #{self.invoice_number}"
    

