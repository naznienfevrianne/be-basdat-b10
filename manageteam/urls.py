from django.urls import path
from manageteam.views import *

app_name = 'manageteam'

urlpatterns = [
    path('daftarTeam/', daftarTeam, name='daftarTeam'),
    path('viewTeam/', viewTeam, name='viewTeam'),
    path('daftarPemain/', daftarPemain, name='daftarPemain'),
    path('daftarPelatih/', daftarPelatih, name='daftarPelatih')
    
]