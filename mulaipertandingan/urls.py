from django.urls import path
from mulaipertandingan.views import *

app_name = 'mulaipertandingan'

urlpatterns = [
    path('listPeristiwa/<uuid:id_pertandingan>/', listPeristiwa, name='listPeristiwa'),
    path('listPeristiwa/<uuid:id_pertandingan>/pilihPeristiwa/<str:nama_tim>/', pilihPeristiwa, name='pilihPeristiwa')
]