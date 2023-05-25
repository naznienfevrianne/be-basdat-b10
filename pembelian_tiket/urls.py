from django.urls import path
from pembelian_tiket.views import *

app_name = 'pembelian_tiket'

urlpatterns = [
    path('pilihStadium/', pilihStadium, name='pilihStadium'),
    path('listWaktu/<str:chosen_stadium>/<str:chosen_date>/', listWaktu, name='listWaktu'),
    path('daftarPertandingan/<str:chosen_stadium>/<str:chosen_date>/', daftarPertandingan, name='daftarPertandingan'),
    path('beliTiket/<str:match>/', beliTiket, name='beliTiket'),
    #path('get_stadium/', get_stadium, name='get_stadium'),
]