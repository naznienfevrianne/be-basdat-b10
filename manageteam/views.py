from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def daftarTeam(request):
    return render(request, 'daftarTeam.html')

def viewTeam(request):
    return render(request, 'viewTeam.html')

def daftarPelatih(request):
    return render(request, 'daftarPelatih.html')

def daftarPemain(request):
    return render(request, 'daftarPemain.html')