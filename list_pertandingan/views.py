#from dj_database_url import parse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection, InternalError
import datetime

# Create your views here.
def list_pertandingan_penonton(request):
    print(request.session['member_type'])
    username = request.session['username']
    print(username)
    cursor = connection.cursor()
    query = """
    SELECT DISTINCT ON (tp1.id_pertandingan) concat(tp1.nama_tim, ' vs ', tp2.nama_tim) AS teams, s.nama,p.start_datetime
    FROM tim_pertandingan tp1
    JOIN tim_pertandingan tp2
    ON tp1.id_pertandingan = tp2.id_pertandingan
    JOIN pertandingan p
    ON tp2.id_pertandingan = p.id_pertandingan
    JOIN stadium s
    ON p.stadium = s.id_stadium
    AND tp1.nama_tim <> tp2.nama_tim;
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    pertandingan = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            # Decode the fetched strings if needed
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        pertandingan.append(detail)

    context = {
        'member_type': 'penonton',
        'pertandingan': pertandingan
    }
    print(context)
    return render (request, 'list_pertandingan_penonton.html',context)

def list_pertandingan_manager(request):
    print(request.session['member_type'])
    username = request.session['username']
    print(username)
    cursor = connection.cursor()
    query = f"""
    SELECT DISTINCT ON (tp1.id_pertandingan) concat(tp1.nama_tim, ' vs ', tp2.nama_tim) AS teams, s.nama,p.start_datetime
    FROM tim_pertandingan tp1
    JOIN tim_pertandingan tp2
    ON tp1.id_pertandingan = tp2.id_pertandingan
    JOIN pertandingan p
    ON tp2.id_pertandingan = p.id_pertandingan
    JOIN stadium s
    ON p.stadium = s.id_stadium
    JOIN tim_manajer tm
    ON tp1.nama_tim = tm.nama_tim
    JOIN manajer m
    ON tm.id_manajer = m.id_manajer
    AND m.username = '{username}'
    AND tp1.nama_tim <> tp2.nama_tim;
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    pertandingan = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            #decode the fetched strings if needed
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        pertandingan.append(detail)

    context = {
        'member_type': 'manajer',
        'pertandingan': pertandingan
    }
    return render (request, 'list_pertandingan_manager.html',context)

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

#def parse(cursor):
#    columns = [col[index] for index, col in enumerate(cursor.description)]
#    return [dict(zip(columns, row)) for row in cursor.fetchall()]