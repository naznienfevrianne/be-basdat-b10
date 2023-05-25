from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def listtandingan(request):
    return render(request, 'listtandingan.html')

def pembuatanPertandingan(request):
    return render(request, 'pembuatanPertandingan.html')

def listWaktuStadium(request):
    return render(request, 'listWaktuStadium.html')

def buatPertandingan(request):
    return render(request, 'buatPertandingan.html')