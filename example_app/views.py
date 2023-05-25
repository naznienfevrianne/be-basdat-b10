from django.shortcuts import render

def index(request):
    try:
        context = {
        'username': request.session['username'],
        'member_type': request.session['member_type']
        }
        return render(request, 'index.html', context)
    except:
        context = {
            'username':'not found'
        }
        return render(request, 'index.html', context)
