from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


from . import views

# router=DefaultRouter()
# router.register('data', Appointment, basename='data')
# urlpatterns=router.urls

app_name='myapp'


urlpatterns = [

    path('home/', views.index, name='home'),
    
    path('home/patient-entry/', views.patient_entry, name="patient_entry"),
    path('home/process-patient-entry/', views.process_patient_entry, name="process_patient_entry"),
    path('home/appointment-receipt/<int:patient_id>/', views.appointment_receipt, name='appointment_receipt'), 
    path('home/api/', views.PatientView.as_view(), name='patient_list' ),
    path('home/api/<int:id>/', views.PatientView.as_view(), name='patient_list' ),
    path('home/api/<int:id>/update/', views.PatientView.as_view()),
    path('home/api/invoices/', views.InvoiceView.as_view(), name="invoice_list" ),
    path('home/api/reports/', views.ReportView.as_view(), name="report"),
    path('home/download-report/', views.download_report, name='download_report'),
    path('home/get-report/<int:report_id>/', views.get_report, name='get_report'),
    path('home/signup/', views.signup, name='signup'),
    path('home/login/', views.login_view, name='login'),
    path('home/logout/', views.logout_view, name='logut'),


    





    path('api/invoice-details/<int:id>/', views.InvoiceView.as_view(), name="invoice_detail"),
    # path('index/', views.jquery, name="jquery"),
    path('datetime/', views.current_datetime, name="current_datetime"),
    

]

urlpatterns=format_suffix_patterns(urlpatterns)
