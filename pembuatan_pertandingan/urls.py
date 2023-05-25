from django.urls import path
from manageteam.views import *
import pembuatan_pertandingan.views as v

app_name = 'pembuatan_pertandingan'

urlpatterns = [
    path('listtandingan/', v.listtandingan, name='listtandingan'),
    path('pembuatanPertandingan/', v.pembuatanPertandingan, name='pembuatanPertandingan'),
    path('listWaktuStadium/', v.listWaktuStadium, name='listWaktuStadium'),
    path('buatPertandingan/', v.buatPertandingan, name='buatPertandingan')
    
]