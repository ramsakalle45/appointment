from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


from . import views

# router=DefaultRouter()
# router.register('data', Appointment, basename='data')
# urlpatterns=router.urls

app_name='myapp'


urlpatterns = [

    path('', views.index, name='home'),
    path('adminsignup/', views.admin_signup_view, name="admin_sign_up_view"),
    path('adminlogin/', views.admin_click_view, name='admin_click_view'),
    path('patient-entry/', views.patient_entry, name="patient_entry"),
    path('process-patient-entry/', views.process_patient_entry, name="process_patient_entry"),
    path('appointment-receipt/<int:patient_id>/', views.appointment_receipt, name='appointment_receipt'), 
    path('api/', views.PatientView.as_view(), name='patient_list' ),
    path('api/<int:id>/', views.PatientView.as_view(), name='patient_list' ),
    path('api/<int:id>/update/', views.PatientView.as_view()),
    path('api/invoices/', views.InvoiceView.as_view(), name="invoice_list" ),
    path('api/reports/', views.ReportView.as_view(), name="report"),
    path('download-report/', views.download_report, name='download_report'),
    path('get-report/<int:report_id>/', views.get_report, name='get_report'),





    path('api/invoice-details/<int:id>/', views.InvoiceView.as_view(), name="invoice_detail"),
    path('index/', views.jquery, name="jquery"),
    path('datetime/', views.current_datetime, name="current_datetime"),
    

]

urlpatterns=format_suffix_patterns(urlpatterns)
