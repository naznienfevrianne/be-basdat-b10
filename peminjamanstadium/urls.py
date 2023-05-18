from django.urls import path
from peminjamanstadium.views import *

app_name = 'peminjamanstadium'

urlpatterns = [
    path('', listPeminjaman, name='listPeminjaman'),
    path('pinjamstadium/', pinjamStadium, name='pinjamStadium'),
    path('pilihwaktu/', pilihwaktu, name='pilih_waktu')
    
]