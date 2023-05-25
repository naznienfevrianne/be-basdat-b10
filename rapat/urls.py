from django.urls import path
from rapat.views import *

app_name = 'rapat'

urlpatterns = [
    path('history/', history_rapat, name='history_rapat')
]