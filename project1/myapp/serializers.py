from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):

  patient_name=serializers.CharField(max_length=200, required=False)
  blood_group=serializers.CharField(max_length=200, required=False)
  patient_age=serializers.IntegerField(required=False)
  disease=serializers.CharField(max_length=200, required=False)
  doctor_name=serializers.CharField(max_length=200, required=False)
  mobile_number=serializers.CharField(max_length=15)
  on_date=serializers.DateField(required=False)

  class Meta:
    
    model=Patient
    fields=('__all__')

