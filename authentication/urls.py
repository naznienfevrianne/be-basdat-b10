from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('register/manajer/', registerManajer, name='registerManajer'),
    path('register/panitia/', registerPanitia, name='registerPanitia'),
    path('register/penonton/', registerPenonton, name='registerPenonton'),
    path('logout/', logout, name='logout')
]