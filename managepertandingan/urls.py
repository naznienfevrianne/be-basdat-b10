from django.urls import path
from managepertandingan.views import *

app_name = 'managepertandingan'

urlpatterns = [
    path('notexist/', notExist, name='notExist'),
    path('listperistiwa/', listPeristiwa, name='listPeristiwa'),
    path('listpertandingan/', listPertandingan, name='listPertandingan'),
    path('listpertandinganconf/', listPertandinganConf, name='listPertandinganConf')
    
]