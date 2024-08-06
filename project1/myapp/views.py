from django.db import models
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
import datetime
from .models import Patient, Invoice  # Import Invoice model
from django.utils.crypto import get_random_string
import random
from weasyprint import HTML
from weasyprint.css import CSS
from django.shortcuts import HttpResponse
from django.urls import reverse

def patient_entry(request):
    return render(request, 'myapp/patient_entry.html')

def process_patient_entry(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        blood_group = request.POST.get('blood_group')
        patient_age = int(request.POST.get('patient_age'))  # Convert to integer
        disease = request.POST.get('disease')
        doctor_name = request.POST.get('doctor_name')
        mobile_number = request.POST.get('mobile_number')
        on_date = request.POST.get('on_date')

        # Create a new patient entry in the database using the Patient model
        patient = Patient(patient_name=patient_name, 
                          blood_group=blood_group, 
                          patient_age=patient_age,
                          disease=disease, 
                          doctor_name=doctor_name,
                          mobile_number=mobile_number,
                          on_date=on_date)
        patient.save()

        # Generate an invoice
        invoice_number = f"INV-{get_random_string(length=6)}"  # Example invoice number format
        items = "Consultation: Rs. 100, Medicine: Rs. 50"  # Example invoice items
        total_amount = 150.00  # Example total amount

        invoice = Invoice(patient=patient,
                          invoice_number=invoice_number,
                          patient_name=patient_name,
                          blood_group=blood_group,
                          patient_age=patient_age,
                          disease=disease,
                          doctor_name=doctor_name,
                          mobile_number=mobile_number,
                          on_date=on_date,
                          items=items,
                          total_amount=total_amount)
        invoice.save()

        # Pass the patient and invoice objects to the template
        return render(request, 'myapp/appointment_receipt.html', {'patient': patient, 'invoice': invoice})



def appointment_receipt(request, patient_id):
    patient=get_object_or_404(Patient, pk=patient_id)
    invoice=Invoice.objects.filter(patient=patient).last()

    #Rneder the template to HTML
    html=render(request, 'myapp/appointment_receipt.html', {'patient':patient, 'invoice':invoice})
    html_string=html.content.decode('utf-8') #convert to a string

    #create pdf
    pdf_file=HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        stylesheets=[CSS(string='@page { size: A4; margin: 2cm; }')])
    # Set the response headers
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return HttpResponseRedirect(reverse('myapp:appointment_receipt', args=[patient_id]))


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer

class PatientView(APIView):

    # def get(self, request, *args, **kwargs):

    #updating get method for fetching data according to the id   
    def get(self, request, id=None): 

        if id:
            try:
                result=Patient.objects.get(id=id)
        
                serializers=PatientSerializer(result)
           
                return Response({'status': 'success', "patient":serializers.data}, status=200)
            except Patient.DoesNotExist:
                return Response({"stutus" : "error", "message":"Patient does not found"}, status=400)
        
        else:
            result=Patient.objects.all()
            serializers=PatientSerializer(result, many=True)
            return Response({'status': 'success', "patient":serializers.data}, status=200)

    

    def post(self, request):

        serializer=PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  


    def patch(self, request, id=None):

        result=Patient.objects.get(id=id)
        serializer=PatientSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data":serializer.data})
        else:
            return Response({"status": "error", "data":serializer.errors})
        


    def delete(self, request, id=None):
        result=get_object_or_404(Patient, id=id)
        result.delete()
        return Response({"status":"success", "data":"Data Deleted"})



























def index(request):
    print(request.GET)
    return render(request,"myapp/home.html")
    # return HttpResponse(request,"hi")
def jquery(request):
    
    print(request.GET)
    return render(request, "myapp/index.html")    

def current_datetime(request):
    now=datetime.datetime.now()
    html="<html><body>It is now %s.</body></html>"%now
    return HttpResponse(html)
