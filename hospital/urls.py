from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("patients/", views.patients_list, name="patients-list"),
    path("patients/<int:pk>/", views.patient_detail),
    
    path("auth/register/", views.register, name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),

    path("doctors/", views.doctors_list),
    path("doctors/<int:pk>/", views.doctor_detail),

    path("mappings/", views.mappings_list),
    path("mappings/<int:patient_id>/", views.mapping_detail),
    path("mappings/<int:pk>/delete/", views.mapping_delete),
]