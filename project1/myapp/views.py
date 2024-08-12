from django.db import models
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
import datetime
from .models import Patient, Invoice, UploadReport  
from django.utils.crypto import get_random_string
import random
from weasyprint import HTML
from weasyprint.css import CSS
from django.shortcuts import HttpResponse
from django.urls import reverse
from random import randint
from django.contrib.auth.decorators import login_required, user_passes_test
from . import forms,models
from django.contrib.auth.models import Group



#for showing signup/login button for admin

def admin_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'myapp/patient_detail_upload.html')    

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('myapp/adminlogin')
    return render(request,'myapp/adminsignup.html',{'form':form})



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
        patient = Patient(
                        patient_name=patient_name, 
                        blood_group=blood_group, 
                        patient_age=patient_age,
                        disease=disease, 
                        doctor_name=doctor_name,
                        mobile_number=mobile_number,
                        on_date=on_date)
        patient.save()


        #     # Generate an invoice
        invoice_number = f"INV-{get_random_string(length=6)}"  
        items = "Consultation: Rs. 100, Medicine: Rs. 50" 
        total_amount = 150.00 

        
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

def download_report(request):

    if request.method=='POST':
        patient_id=request.POST.get('patient_id')
        report_name=request.POST.get('report_name')
        reports=request.POST.get('reports')
        upload_date=request.POST.get('upload_date')

        report=UploadReport(
            patient_id=patie
        )

    

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.http import HttpResponse

def appointment_receipt(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    invoice = Invoice.objects.filter(patient=patient).last()

    # Create a canvas object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    c = canvas.Canvas(response, pagesize=A4)

    # Define styles for invoice elements
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontSize=24, alignment=1, bold=True)
    heading_style = ParagraphStyle(name='Heading', fontSize=16, alignment=0, bold=True)
    body_style = styles['Normal']

    # Draw invoice header
    c.drawString(inch, 10.5 * inch, "Appointment Receipt")

    # Draw patient information
    c.drawString(inch, 10 * inch, f"Patient Name: {patient.patient_name}")
    c.drawString(inch, 9.5 * inch, f"Blood Group: {patient.blood_group}")
    c.drawString(inch, 9 * inch, f"Age: {patient.patient_age}")
    c.drawString(inch, 8.5 * inch, f"Disease: {patient.disease}")
    c.drawString(inch, 8 * inch, f"Doctor: {patient.doctor_name}")
    c.drawString(inch, 7.5 * inch, f"Mobile Number: {patient.mobile_number}")

    # Draw invoice details
    c.drawString(inch, 7 * inch, "Invoice Details")
    c.drawString(inch, 6.5 * inch, f"Invoice Number: {invoice.invoice_number}")
    c.drawString(inch, 6 * inch, f"On Date: {invoice.on_date}")
    c.drawString(inch, 5.5 * inch, f"Items: {invoice.items}")

    # Draw total amount
    c.drawString(inch, 5 * inch, f"Total Amount: {invoice.total_amount}")

    # Save the PDF
    c.showPage()
    c.save()
    return response
    
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer, InvoiceSerializer, ReportSerializer

class PatientView(APIView):

    # def get(self, request, *args, **kwargs):

    #updating get method for fetching data according to the id   
    def get(self, request, id=None, format=None): 

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

    

    def post(self, request, format=None):

        serializer=PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  


    def patch(self, request, id=None, format=None):

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

class InvoiceView(APIView):
    def get(self, request, id=None, format=None):
        
        if id:
            try:
                result=Invoice.objects.get(id=id)
                serializer=InvoiceSerializer(result)
                return Response({"status": "success", "data":serializer.data}, status=200)
            except Invoice.DoesNotExist:
                return Response({"status": "error", "message":"Invoice does not exit"})
            

        else:
            result=Invoice.objects.all()
            serializer=InvoiceSerializer(result, many=True)
            return Response({"status": "success", "data":serializer.data}, status=200)
        

class ReportView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                result=UploadReport.objects.get(id=id)
                serializer=ReportSerializer(result, many=True)
                return Response({"status": "success", "data":serializer.data}, status=200)
            except UploadReport.DoesNotExist:
                return Response({"status": "error", "message": "Report does not exist"}) 
                   
        else:
            result=UploadReport.objects.all()
            serializer=ReportSerializer(result, many=True)
            return Response({"status": "success", "data":serializer.data}, status=200)
            
        

            

        

























def index(request):
    print(request.GET)
    return render(request,"myapp/index.html")
    # return HttpResponse(request,"hi")
def jquery(request):
    
    print(request.GET)
    return render(request, "myapp/home.html")    

def current_datetime(request):
    now=datetime.datetime.now()
    html="<html><body>It is now %s.</body></html>"%now
    return HttpResponse(html)
