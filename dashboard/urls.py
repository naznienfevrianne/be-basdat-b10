from django.urls import path
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('manajer/', dashboardManajer, name='dashboardManajer'),
    path('panitia/', dashboardPanitia, name='dashboardPanitia'),
    path('penonton/', dashboardPenonton, name='dashboardPenonton')

    
]