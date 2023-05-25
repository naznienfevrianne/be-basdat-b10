from django.shortcuts import render
from django.db import connection

# Create your views here.
def history_rapat(request):
    username = request.session['username']
    cursor = connection.cursor()
    query = f"""
    SELECT DISTINCT ON (tp1.id_pertandingan) concat(tp1.nama_tim, ' vs ', tp2.nama_tim) AS teams, concat(np.nama_depan,' ',np.nama_belakang) AS nama_panitia, 
    s.nama AS nama_stadium, r.datetime, r.isi_rapat
    FROM tim_pertandingan tp1
    JOIN tim_pertandingan tp2
    ON tp1.id_pertandingan = tp2.id_pertandingan
    JOIN rapat r
    ON tp2.id_pertandingan = r.id_pertandingan
    JOIN non_pemain np
    ON r.perwakilan_panitia = np.id
    JOIN pertandingan p
    ON r.id_pertandingan = p.id_pertandingan
    JOIN stadium S
    ON p.stadium = s.id_stadium
    AND tp1.nama_tim <> tp2.nama_tim;
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    history_rapat = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            #decode the fetched strings if needed
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        history_rapat.append(detail)

    context = {
        'member_type': 'manajer',
        'history_rapat': history_rapat
    }
    return render (request, 'history_rapat.html',context)


def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

#<th><a class="link" href="https://example.com"><u>Lihat Catatan Rapat</u></a></th>