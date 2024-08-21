from django.db import models
from rest_framework import serializers
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Add unique=True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove username from REQUIRED_FIELDS
    def __str__(self):
        return self.email
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',  # Add related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',  # Add related_name
    
    )

departments=[('Cardiology', 'Cardiology'), ('Dermatology', 'Dermatology'),
             ('Emergency Medicine', 'Emergency Medicine'),
             ('Gestroenterology', 'Gestroenterology'),
             ('Nuerology', 'Nuerology')]

class Doctor(models.Model):
    user=models.ManyToManyField(User, on_delete=models.CASCADE)

    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    mobile_number=models.PositiveIntegerField(max_length=20, null=False, blank=False)
    address=models.CharField(max_length=100, null=True, blank=True)
    department=models.CharField(max_length=40, choices=departments, default='Cardiology')
    education=models.CharField(max_length=20, null=True, blank=True)
    
    @property
    def get_name(self):
        return self.user.doctor_name+" "+self.user.department
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.user.department)
    


     

class Patient(models.Model):


    user=models.ManyToManyField(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=200, null=True, blank=True)
    blood_group = models.CharField(max_length=200, null=True,blank=True)
    patient_age=models.IntegerField(null=True, blank=True)
    disease=models.CharField(max_length=100, null=True, blank=True)
    department=models.CharField(max_length=20, choices=departments, default="Cardiology")
    doctor_name=models.CharField(max_length=100, null=True, blank=True)
    mobile_number=models.IntegerField(null=True, blank=True)
    on_date=models.DateField(null=True, blank=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.disease+")"
    
class Invoice(models.Model):
    user= models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    patient_name = models.CharField(max_length=200, null=True,
   blank=True)
    blood_group = models.CharField(max_length=200, null=True,
   blank=True)
    patient_age=models.IntegerField(null=True, blank=True)
    department=models.CharField(max_length=20, null=True, blank=True)
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
    user=models.ManyToManyField(User, on_delete=models.CASCADE)
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
    
class Discharge_Summary(models.Model):

    user=models.OneToOneField(Patient, on_delete=models.CASCADE)
    
    patient_id=models.PositiveIntegerField(max_length=20, unique=True, null=False, blank=False)
    mobile_number=models.PositiveIntegerField(max_length=20, null=True, blank=True)
    patient_name=models.CharField(max_length=20, null=True, blank=True)
    doctor_name=models.CharField(max_length=20, null=True, blank=True)
    disease=models.CharField(max_length=40, null=True, blank=True)
    department=models.CharField(max_length=40, choices=departments, default="Cardiology")
    admission_date=models.DateField(null=False)
    admission_time=models.TimeField(null=False)
    release_date=models.DateField(null=False)
    release_time=models.TimeField(null=False)
    prescription=models.FileField(null=True)
    room_charge=models.IntegerField(null=True, blank=True)
    bed_charge=models.PositiveIntegerField(null=True, blank=True)
    doctor_fee=models.PositiveIntegerField(null=True, blank=True)
    total_amount=models.PositiveIntegerField(null=True, blank=True)


    




    
    
    

