from django.urls import path
from rapat.views import *

app_name = 'rapat'

urlpatterns = [
    path('history/', history_rapat, name='list_pertandingan_penonton')
]