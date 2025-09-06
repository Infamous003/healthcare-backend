from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("patients/", views.patients_list),
    path("patients/<int:pk>/", views.patient_detail),
    
    path("auth/register/", views.register, name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),

    path("doctors/", views.doctors_list),
    path("doctors/<int:pk>/", views.doctor_detail),
]