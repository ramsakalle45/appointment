from django.db import models
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
import datetime
from .models import Patient, Invoice, UploadReport, CustomUser, Doctor, Discharge_Summary
from django.utils.crypto import get_random_string
import random
from weasyprint import HTML
from weasyprint.css import CSS
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def index(request):
    # print(request.GET)
    return render(request,"myapp/index.html")
 

#for showing signup/login button for admin

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            messages.success(request, 'Account created successfully.')
            return redirect(reverse('myapp:login'))  # Redirect to login page
        else:
            messages.error(request, 'Invalid signup details.')
            return render(request, 'myapp/adminsignup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'myapp/adminsignup.html', {'form': form})
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return render(request, 'myapp/patient_report.html')  # Redirect to admin panel
            else:
                messages.error(request, 'Invalid credentials.')
                return render(request, 'myapp/adminlogin.html', {'form': form})
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'myapp/adminlogin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'myapp/adminlogin.html', {'form': form})
    

def logout_view(request):
    logout(request)
    messages.success('Loggedout successfuly')
    return redirect('myapp:home')    


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
                        department=department,
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
                        department=department,
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

    """Fetches patient reports based on patient_id entered manually."""
   
    reports = None
    patient_id = None
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            reports = UploadReport.objects.filter(patient_id=patient_id)  # Fetch reports based on patient_id
    context = {
        'reports': reports,
        'patient_id': patient_id,  # Pass the patient_id to the template
    }
    return render(request, 'myapp/patient_report.html', context)

def get_report(request, report_id):
    
    report=get_object_or_404(UploadReport, pk=report_id)
    response=HttpResponse(report.reports.read(),content_type="application/pdf" )
    response['Content-Disposition']=f'attachment; filename="{report.report_name}"'
    return response

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
    c.drawString(inch, 11.5 * inch, "Appointment Receipt")

    # Draw patient information
    c.drawString(inch, 11 * inch, f"Patient ID: {invoice.id}")
    c.drawString(inch, 10.5 * inch, f"Patient Name: {patient.patient_name}")
    c.drawString(inch, 10 * inch, f"Blood Group: {patient.blood_group}")
    c.drawString(inch, 9.5 * inch, f"Age: {patient.patient_age}")
    c.drawString(inch, 9 * inch, f"Disease: {patient.disease}")
    c.drawString(inch, 8.5 * inch, f"Doctor: {patient.doctor_name}")
    
    c.drawString(inch, 8 * inch, f"Doctor: {patient.department}")
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
            
        

            

        


























def jquery(request):
    
    print(request.GET)
    return render(request, "myapp/home.html")    

def current_datetime(request):
    now=datetime.datetime.now()
    html="<html><body>It is now %s.</body></html>"%now
    return HttpResponse(html)
