from django.urls import path
from manageteam.views import *
import mulai_rapat.views as v

app_name = 'mulai_rapat'

urlpatterns = [
    path('pilihPertandingan/', v.pilihPertandingan, name='pilihPertandingan'),
    path('rapatPertandingan/<str:chosen_rapat>/', v.rapatPertandingan, name='rapatPertandingan'),
]