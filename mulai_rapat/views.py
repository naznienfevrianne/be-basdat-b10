# Create your views here.
from django.shortcuts import render

# Create your views here.
def pilihPertandingan(request):
    return render(request, 'pilihPertandingan.html')

def rapatPertandingan(request):
    return render(request, 'rapatPertandingan.html')

