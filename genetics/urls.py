from django.urls import path
from .views import dna_diagnosis


app_name = 'genetics'

urlpatterns = [
     path('dna_diagnosis/', dna_diagnosis, name='dna_diagnosis'),
     
]
