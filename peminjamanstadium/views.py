from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def listPeminjaman(request):
    return render(request, 'listpeminjaman.html')

def pinjamStadium(request):
    return render(request, 'pinjamStadium.html')

def pilihwaktu(request):
    return render(request, 'pilihwaktu.html')
