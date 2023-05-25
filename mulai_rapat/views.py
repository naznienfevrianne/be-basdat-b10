# Create your views here.
import random
import string
from django.shortcuts import redirect, render
from django.db import connection, InternalError
from django.urls import reverse
from django.contrib import messages
import datetime

# Create your views here.
def pilihPertandingan(request):
    print(request.session['member_type'])
    username = request.session['username']
    print(username)

    query = f"""
    SELECT DISTINCT ON (tp1.id_pertandingan) concat(tp1.nama_tim, ' vs ', tp2.nama_tim) as teams, s.nama as nama_stadium, p.start_datetime, p.end_datetime, p.id_pertandingan, tp1.nama_tim as nama_tim1, tp2.nama_tim as nama_tim2
    FROM tim_pertandingan tp1
    JOIN tim_pertandingan tp2
    ON tp1.id_pertandingan = tp2.id_pertandingan
    JOIN pertandingan p
    ON tp2.id_pertandingan = p.id_pertandingan
    JOIN stadium s
    ON p.stadium = s.id_stadium
    JOIN tim_manajer tm
    ON tp1.nama_tim = tm.nama_tim
    AND tp1.nama_tim <> tp2.nama_tim
    AND tp1.id_pertandingan NOT IN (SELECT id_pertandingan FROM RAPAT);
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

def rapatPertandingan(request, chosen_rapat, nama_tim1, nama_tim2):
    print(request.session['member_type'])
    username = request.session['username']
    print(username)
    print('--------------------')
    print(chosen_rapat)

    if request.method == 'POST':
        id_pertandingan = chosen_rapat
        tanggal_rapat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(tanggal_rapat)

        query_panitia = f"""
        SELECT pa.id_panitia
        FROM panitia pa
        WHERE pa.username = '{username}'
        """
        cursor = connection.cursor()
        cursor.execute('set search_path to public')
        cursor.execute(query_panitia)
        res = parse(cursor)
        for p in res:
            detail = {}
            for attr, value in p.items():
                # Decode the fetched strings if needed
                if isinstance(value, bytes):
                    value = value.decode()
                detail[attr] = value
        
        perwakilan_panitia = detail['id_panitia']
        print(perwakilan_panitia)

        print('cek nama tim 1')
        print(nama_tim1)

        query_manager_tim1 = f"""
        SELECT m.id_manajer
        FROM manajer m, tim_manajer tm
        WHERE tm.id_manajer = m.id_manajer
        AND tm.nama_tim = '{nama_tim1}'
        """
        cursor.execute('set search_path to public')
        cursor.execute(query_manager_tim1)
        res = parse(cursor)
        for p in res:
            detail = {}
            for attr, value in p.items():
                # Decode the fetched strings if needed
                if isinstance(value, bytes):
                    value = value.decode()
                detail[attr] = value
        
        manajer_tim_a = detail['id_manajer']
        print(manajer_tim_a)

        query_manager_tim2 = f"""
        SELECT m.id_manajer
        FROM manajer m, tim_manajer tm
        WHERE tm.id_manajer = m.id_manajer
        AND tm.nama_tim = '{nama_tim2}'
        """
        cursor.execute('set search_path to public')
        cursor.execute(query_manager_tim2)
        res = parse(cursor)
        for p in res:
            detail = {}
            for attr, value in p.items():
                # Decode the fetched strings if needed
                if isinstance(value, bytes):
                    value = value.decode()
                detail[attr] = value
        
        manajer_tim_b = detail['id_manajer']
        print(manajer_tim_b)

        isi_rapat = request.POST.get('isi_rapat')

        insert_query = f"""
        INSERT INTO RAPAT VALUES('{id_pertandingan}','{tanggal_rapat}','{perwakilan_panitia}','{manajer_tim_a}','{manajer_tim_b}','{isi_rapat}')
        """
        try:
            cursor.execute('set search_path to public')
            cursor.execute(insert_query)
            return redirect('dashboard:show_dashboard')
        
        except InternalError as e: 
            messages.info(request, str(e.args))

    context = {
        'member_type': 'manajer',
        'tim1': nama_tim1,
        'tim2': nama_tim2
    }

    print(context)

    return render(request, 'rapatPertandingan.html', context)

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]