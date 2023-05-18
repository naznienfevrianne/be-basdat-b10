from django.shortcuts import render

# Create your views here.
def dashboardManajer(request):
    return render(request, 'dashboardManajer.html')

def dashboardPanitia(request):
    return render(request, 'dashboardPanitia.html')

def dashboardPenonton(request):
    return render(request, 'dashboardPenonton.html')