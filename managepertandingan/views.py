from django.shortcuts import render

# Create your views here.
def listPeristiwa(request):
    return render(request, 'listPeristiwa.html')

def listPertandingan(request):
    return render(request, 'listPertandingan.html')

def notExist(request):
    return render(request, 'notExist.html')

def listPertandinganConf(request):
    return render(request, 'listPertandinganConf.html')