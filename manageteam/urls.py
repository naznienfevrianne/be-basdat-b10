from django.urls import path
from manageteam.views import *

app_name = 'manageteam'

urlpatterns = [
    path('daftarTeam/', daftarTeam, name='daftarTeam'),
    path('viewTeam/', viewTeam, name='viewTeam'),
    path('daftarPemain/<str:nama_tim>', daftarPemain, name='daftarPemain'),
    path('daftarPelatih/<str:nama_tim>', daftarPelatih, name='daftarPelatih'),
    path('deletePemain/<str:id_pemain>', deletePemain, name='deletePemain'),
    path('deletePelatih/<str:id_pelatih>', deletePelatih, name='deletePelatih'),
    path('makeCaptainPemain/<str:id_pemain>/<str:nama_tim>', makeCaptainPemain, name='makeCaptainPemain')
]