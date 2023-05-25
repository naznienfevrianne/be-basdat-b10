# Create your views here.
import random
import string
from django.shortcuts import redirect, render
from django.db import connection, InternalError
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def pilihPertandingan(request):
    print(request.session['member_type'])
    username = request.session['username']
    print(username)

    query = f"""
        SELECT DISTINCT ON (tp1.id_pertandingan) concat(tp1.nama_tim, ' vs ', tp2.nama_tim) as teams, s.nama as nama_stadium, p.start_datetime, p.end_datetime, p.id_pertandingan
        FROM tim_pertandingan tp1
        JOIN tim_pertandingan tp2
        ON tp1.id_pertandingan = tp2.id_pertandingan
        JOIN pertandingan p
        ON tp2.id_pertandingan = p.id_pertandingan
        JOIN stadium s
        ON p.stadium = s.id_stadium
        JOIN tim_manajer tm
        ON tp1.nama_tim = tm.nama_tim
        AND tp1.nama_tim <> tp2.nama_tim;
    """

    cursor = connection.cursor()
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)

    matches = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            # Decode the fetched strings if needed
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        matches.append(detail)

    context = {
        'member_type': 'manajer',
        'matches': matches,
    }

    print(context)


    return render(request, 'pilihPertandingan.html', context)

def rapatPertandingan(request, chosen_rapat):
    print(request.session['member_type'])
    username = request.session['username']
    print(username)
    print(chosen_rapat)

    query = f"""
        SELECT DISTINCT ON (tp1.id_pertandingan) concat(tp1.nama_tim, ' vs ', tp2.nama_tim) as teams
        FROM tim_pertandingan tp1
        JOIN tim_pertandingan tp2
        ON tp1.id_pertandingan = tp2.id_pertandingan
        JOIN pertandingan p
        ON tp2.id_pertandingan = p.id_pertandingan
        JOIN stadium s
        ON p.stadium = s.id_stadium
        JOIN rapat r
        ON r.id_pertandingan = '{chosen_rapat}'
        JOIN panitia px
        ON px.id_panitia = r.perwakilan_panitia
        AND px.username = '{username}'
    """

    # AND m.username = '{username}'

    cursor = connection.cursor()
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)

    # match = []
    # for p in res:
    #     detail = {}
    #     for attr, value in p.items():
    #         # Decode the fetched strings if needed
    #         if isinstance(value, bytes):
    #             value = value.decode()
    #         detail[attr] = value
    #     match.append(detail)

    context = {
        'member_type': 'manajer',
        'match_name': res[0]["teams"],
    }

    print('test')

    print(context)

    return render(request, 'rapatPertandingan.html', context)

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]