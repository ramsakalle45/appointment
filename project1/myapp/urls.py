from django.urls import path

from . import views

app_name='myapp'

urlpatterns = [

    path('', views.index, name='home'),
    path('patient-entry/', views.patient_entry, name="patient_entry"),
    path('process-patient-entry/', views.process_patient_entry, name="process_patient_entry"),
    path('api/', views.PatientView.as_view(), name='patient_list' ),
    path('api/<int:id>/', views.PatientView.as_view(), name='patient_list' )
    
   
    # path('index/', views.jquery, name="jquery"),
    # path('datetime/', views.current_datetime, name="current_datetime"),
    

]
