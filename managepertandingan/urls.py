from django.urls import path
from managepertandingan.views import *

app_name = 'managepertandingan'

urlpatterns = [
    path('notexist/', notExist, name='notExist'),
    path('listpertandingan/', listPertandingan, name='listPertandingan'),
    path('listpertandinganconf/', listPertandinganConf, name='listPertandinganConf'),
    path('listPeristiwa/<uuid:id_pertandingan>/<str:nama_tim>/', listPeristiwa, name='listPeristiwa'),

]