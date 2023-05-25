from django.shortcuts import render, redirect
from django.db import connection, InternalError
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def listPeristiwa(request, id_pertandingan, nama_tim):
    query_peristiwa = f"""
        SELECT *
        FROM PEMAIN AS pm
        JOIN PERISTIWA AS ps ON pm.id_pemain = ps.id_pemain
        WHERE pm.nama_tim = '{nama_tim}'
        AND ps.id_pertandingan = '{id_pertandingan}';
        """
    
    cursor = connection.cursor()
    cursor.execute(query_peristiwa)
    peristiwa_pertandingan = fetch(cursor)

    print(id_pertandingan)
    print(nama_tim)
    print(peristiwa_pertandingan)

    context = {
        'member_type': 'panitia',
        'nama_tim' : nama_tim,
        'peristiwa_pertandingan' : peristiwa_pertandingan
    }

    return render(request, 'listPeristiwa.html', context)

def listPertandingan(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to public")
    cursor.execute("""SELECT pertandingan.id_pertandingan, ARRAY_AGG(tim_pertandingan.nama_tim) as tim, start_datetime, end_datetime
        FROM pertandingan, tim_pertandingan
        WHERE pertandingan.id_pertandingan=tim_pertandingan.id_pertandingan
        GROUP BY pertandingan.id_pertandingan
        ORDER BY start_datetime asc""")
    pertandingan = cursor.fetchall()

    pemenang = {}
    for p in pertandingan:    
        query_jumlah_pertandingan = f"""
        SELECT COUNT(*) as jumlah_pertandingan
        FROM PERTANDINGAN;
        """
    cursor = connection.cursor()
    cursor.execute(query_jumlah_pertandingan)
    jumlah_pertandingan = fetch(cursor)

    query_pertandingan = f"""
        SELECT pertandingan.id_pertandingan, ARRAY_AGG(tim_pertandingan.nama_tim) as tim, start_datetime
        FROM pertandingan, tim_pertandingan
        WHERE pertandingan.id_pertandingan=tim_pertandingan.id_pertandingan
        GROUP BY pertandingan.id_pertandingan
        ORDER BY start_datetime;
        """
    cursor = connection.cursor()
    cursor.execute(query_pertandingan)
    pertandingan = fetch(cursor)
    
    pemenang = {}
    for i in pertandingan:
        query_skor = f"""
            SELECT nama_tim, skor
            FROM TIM_PERTANDINGAN
            WHERE id_pertandingan = '{i['id_pertandingan']}';
            """
        cursor = connection.cursor()
        cursor.execute(query_skor)
        skor_pertandingan = fetch(cursor)

        if skor_pertandingan[0]['skor'] > skor_pertandingan[1]['skor']:
            pemenang[i['id_pertandingan']] = skor_pertandingan[0]['nama_tim']
        elif skor_pertandingan[1]['skor'] > skor_pertandingan[0]['skor']:
            pemenang[i['id_pertandingan']] = skor_pertandingan[1]['nama_tim']
        else:
            pemenang[i['id_pertandingan']] = "SERI"

    context = {
        'member_type': 'panitia',
        'jumlah_pertandingan': jumlah_pertandingan[0]['jumlah_pertandingan'],
        'pertandingan': pertandingan,
        'pemenang' : pemenang
    }

    return render(request, 'listPertandingan.html', context)

def notExist(request):
    return render(request, 'notExist.html')

def listPertandinganConf(request):
    return render(request, 'listPertandinganConf.html')

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
