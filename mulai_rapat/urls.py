from django.urls import path
from manageteam.views import *
import mulai_rapat.views as v

app_name = 'mulai_rapat'

urlpatterns = [
    path('pilihPertandingan/', v.pilihPertandingan, name='pilihPertandingan'),
    path('rapatPertandingan/<str:chosen_rapat>/<str:nama_tim1>/<str:nama_tim2>', v.rapatPertandingan, name='rapatPertandingan'),
]