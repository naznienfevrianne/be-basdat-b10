from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from authentication.forms import *

def login(request):
    
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')

def registerManajer(request):
    return render(request, 'registerManajer.html')

def registerPanitia(request):
    return render(request, 'registerPanitia.html')

def registerPenonton(request):
    return render(request, 'registerPenonton.html')