# Create your views here.
import random
import string
from django.shortcuts import redirect, render
from django.db import connection, InternalError
from django.urls import reverse
from django.contrib import messages


def listPeminjaman(request):
    print(request.session['member_type'])
    username = request.session['username']
    print(username)

    query = f"""
        SELECT s.nama AS stadium, concat(p.start_datetime, '  s/d  ', p.end_datetime) as waktu
        FROM stadium s, peminjaman p, manajer m
        WHERE s.id_stadium = p.id_stadium
        AND p.id_manajer = m.id_manajer AND m.username = '{username}';
    """

    cursor = connection.cursor()
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)

    borrow = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            # Decode the fetched strings if needed
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        borrow.append(detail)

    context = {
        'member_type': 'manajer',
        'borrow': borrow,
    }

    print(context)
    return render(request, 'listpeminjaman.html',context)

def pinjamStadium(request):
    if request.method == 'POST':
       
        chosen_stadium = request.POST.get('chosen_stadium')
    #page view
    context = {'member_type':'manajer'}

    username = request.session['username']
    cursor = connection.cursor()
    query = f"""
    SELECT id_stadium, nama FROM Stadium
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    stadium = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            # Decode the fetched strings if needed
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        stadium.append(detail)

    context['stadium'] = stadium
    print(context)
   
    return render(request, 'pinjamStadium.html', context)

def pilihwaktu(request):
    

    return render(request, 'pilihwaktu.html')


def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]