import random
import string
from django.shortcuts import redirect, render
from django.db import connection, InternalError
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def pilihStadium(request):
    if request.method == 'POST':
        print('masuk sini ga')
        chosen_stadium = request.POST.get('chosen_stadium')
        chosen_date = request.POST.get('date')
        print(chosen_stadium)
        return redirect(reverse('pembelian_tiket:daftarPertandingan', args=[chosen_stadium, chosen_date]))
    
    #page view
    context = {'member_type':'penonton'}

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
    
    return render(request, 'pilihStadium.html',context)

#tidak ada di deskripsi paragraf soal, tetapi ada tabelnya di pdf(?)
def listWaktu(request, chosen_stadium, chosen_date):
    print('masuk di list waktu')
    print(chosen_stadium)
    print(chosen_date)

    query = f"""
    SELECT generate_series('{chosen_date}'::date, p.end_datetime::date, '1 day')::date AS date_range
    FROM pertandingan p, stadium s
    WHERE p.stadium = s.id_stadium
    AND s.nama = '{chosen_stadium}';
    """
    cursor = connection.cursor()
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    schedules = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            # Decode the fetched strings if needed
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        schedules.append(detail)

    context = {
        'member_type': 'penonton',
        'chosen_stadium': chosen_stadium,
        'chosen_date': chosen_date,
        'schedules' : schedules
    }
    return render(request, 'listWaktu.html', context)

def daftarPertandingan(request, chosen_stadium, chosen_date):
    if request.method == 'POST':
        match = request.POST.get('match')
        print('dapet ga')
        print(match)
        return redirect(reverse('pembelian_tiket:beliTiket', args=[match]))
    
    query = f"""
    SELECT DISTINCT ON (tp1.id_pertandingan) tp1.nama_tim as tim1, tp2.nama_tim as tim2, tp1.id_pertandingan as id
    FROM tim_pertandingan tp1
    JOIN tim_pertandingan tp2
    ON tp1.id_pertandingan = tp2.id_pertandingan
    JOIN pertandingan p
    ON tp2.id_pertandingan = p.id_pertandingan
    JOIN stadium s
    ON p.stadium = s.id_stadium
    AND tp1.nama_tim <> tp2.nama_tim
    AND s.nama = '{chosen_stadium}'
    AND '{chosen_date}' BETWEEN p.start_datetime AND end_datetime;
    """
    cursor = connection.cursor()
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    schedules = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            # Decode the fetched strings if needed
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        schedules.append(detail)

    context = {
        'member_type': 'penonton',
        'chosen_stadium': chosen_stadium,
        'chosen_date': chosen_date,
        'schedules' : schedules
    }
    return render(request, 'daftarPertandingan.html',context)

def beliTiket(request,match):
    username = request.session['username']
    random_varchar = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    print(random_varchar)

    #for insert data
    if request.method == 'POST':
        jenis_tiket = request.POST.get('jenis_tiket') #not null
        jenis_pembayaran = request.POST.get('jenis_pembayaran') #not null
        id_pertandingan = match #FK
        
        random_varchar = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        nomor_receipt = random_varchar #PK

        #get user's id_penonton
        cursor = connection.cursor()
        query = f"""
        SELECT id_penonton FROM penonton where username = '{username}'
        """
        cursor.execute('set search_path to public')
        cursor.execute(query)
        res = parse(cursor)
        for p in res:
            detail = {}
            for attr, value in p.items():
                # Decode the fetched strings if needed
                if isinstance(value, bytes):
                    value = value.decode()
                detail[attr] = value
        
        id_penonton = detail['id_penonton'] #FK

        insert_query = f"""
        INSERT INTO PEMBELIAN_TIKET VALUES ('{nomor_receipt}','{id_penonton}','{jenis_tiket}','{jenis_pembayaran}','{id_pertandingan}')
        """
        try:
            cursor.execute('set search_path to public')
            cursor.execute(insert_query)
            return redirect('dashboard:show_dashboard')
        
        except InternalError as e: 
            messages.info(request, str(e.args))

    context = {
        'member_type' : 'penonton'
    }
    return render(request, 'beliTiket.html',context)

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]