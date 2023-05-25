from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

# Create your views here.
def listPeristiwa(request, id_pertandingan):
    query = f"""
        SELECT ARRAY_AGG(nama_tim) as nama_tim, id_pertandingan
        FROM tim_pertandingan
        WHERE id_pertandingan='{id_pertandingan}'
        GROUP BY id_pertandingan;
        """
    cursor = connection.cursor()
    cursor.execute(query)
    data = fetch(cursor)

    context = {
        'member_type': 'panitia',
        "data": data[0]
    }

    return render(request, 'listPeristiwa.html', context)

def pilihPeristiwa(request, id_pertandingan, nama_tim):
    if request.method == "POST":
        pemain1 = request.POST.get('pemain1') 
        pemain2 = request.POST.get('pemain2')
        pemain3 = request.POST.get('pemain3') 
        pemain4 = request.POST.get('pemain4')
        pemain5 = request.POST.get('pemain5')  
        peristiwa1 = request.POST.get('peristiwa1') 
        peristiwa2 = request.POST.get('peristiwa2') 
        peristiwa3 = request.POST.get('peristiwa3') 
        peristiwa4 = request.POST.get('peristiwa4') 
        peristiwa5 = request.POST.get('peristiwa5')
        waktu1 = str(request.POST.get('waktu1')).replace("T", " ") + ":00"
        waktu2 = str(request.POST.get('waktu2')).replace("T", " ") + ":00"
        waktu3 = str(request.POST.get('waktu3')).replace("T", " ") + ":00"
        waktu4 = str(request.POST.get('waktu4')).replace("T", " ") + ":00"
        waktu5 = str(request.POST.get('waktu5')).replace("T", " ") + ":00"
        peristiwaList = [[pemain1, peristiwa1, waktu1], [pemain2, peristiwa2, waktu2], [pemain3, peristiwa3, waktu3], [pemain4, peristiwa4, waktu4], [pemain5, peristiwa5, waktu5]]

        print(peristiwaList)

        for data in peristiwaList:
            if data[0] == 0 or data[1] == 0 or len(data[2]) < 19:
                continue
            else:
                query = f"""
                    INSERT INTO peristiwa VALUES(
                    '{id_pertandingan}', '{data[2]}', '{data[1]}', '{data[0]}'
                    );
                    """
                cursor = connection.cursor()
                cursor.execute(query)
                insertData = fetch(cursor)

        if type(insertData) != int  :
            return JsonResponse({'success': 'false', 'message': 'Fail'}, status = 200)
        else:
            return JsonResponse({'success': 'true', 'message': 'Succeed'}, status=200)        
    else:
        query = f"""
            SELECT pertandingan.id_pertandingan, tim_pertandingan.nama_tim, JSON_AGG(JSON_BUILD_ARRAY(id_pemain, pemain.nama_depan, pemain.nama_belakang)) as nama_pemain
            FROM pertandingan, tim_pertandingan, pemain
            WHERE pertandingan.id_pertandingan=tim_pertandingan.id_pertandingan
            AND tim_pertandingan.nama_tim=pemain.nama_tim
            AND pertandingan.id_pertandingan='{id_pertandingan}'
            AND tim_pertandingan.nama_tim='{nama_tim}'
            GROUP BY pertandingan.id_pertandingan, tim_pertandingan.nama_tim;
            """
        cursor = connection.cursor()
        cursor.execute(query)
        data = fetch(cursor)
        
        context = {
            'member_type': 'panitia',
            'data': data[0]
        }

    return render(request, 'pilihPeristiwa.html',context)

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]