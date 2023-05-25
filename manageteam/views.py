from django.shortcuts import render, redirect
from django.db import connection, InternalError
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import uuid

def viewTeam(request):
    username = request.session['username']
    cursor = connection.cursor()
    query = f"""
    select id_manajer
    from manajer M
    where username = '{username}'
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    manajer = res[0]
    id_manajer = manajer['id_manajer']
    query2 = f"""
    select nama_tim
    from tim_manajer
    where id_manajer = '{id_manajer}';
    """
    cursor.execute(query2)
    res2 = parse(cursor)
    
    if len(res2) == 1:
        tim = res2[0]
        nama_tim = tim['nama_tim']
        query3 = f"""
        SELECT id_pemain, nama_depan, nama_belakang, pemain, nomor_hp, tgl_lahir,
        is_captain, posisi, npm, jenjang
        from pemain
        where nama_tim = '{nama_tim}';
        """
        cursor.execute(query3)
        res3 = parse(cursor)
        
        players = []
        for pemain in res3:
            pemain_detail = {}
            for attr in pemain:
                if isinstance(pemain[attr], datetime.date):
                    formatted_date = pemain[attr].strftime("%d-%m-%Y")
                    pemain_detail[attr] = formatted_date
                else:
                    pemain_detail[attr] = str(pemain[attr])
            players.append(pemain_detail)
        print('playersssss ' + str(players))
        query4 = f"""
        SELECT distinct p.id_pelatih, nomor_hp, nama_depan, nama_belakang, email, alamat,
        spesialisasi
        FROM pelatih P, spesialisasi_pelatih S, non_pemain N
        where p.nama_tim = '{nama_tim}' and p.id_pelatih = n.id
        and p.id_pelatih = s.id_pelatih;
        """
        cursor2 = connection.cursor()
        cursor2.execute(query4)
        res4 = parse(cursor2)
        coaches = []
        for pelatih in res4:
            pelatih_detail = {}
            for attr in pelatih:
                if isinstance(pelatih[attr], datetime.date):
                    formatted_date = pelatih[attr].strftime("%d-%m-%Y")
                    pelatih_detail[attr] = formatted_date
                else:
                    pelatih_detail[attr] = pelatih[attr]
            coaches.append(pelatih_detail)
        context = {
            'players': players,
            'coaches': coaches,
            'username':request.session['username'],
            'member_type':request.session['member_type'],
            'nama_tim':nama_tim
        }
        return render(request, 'viewTeam.html', context)
    else:
        response = HttpResponseRedirect(reverse('manageteam:daftarTeam'))
        return response

def daftarTeam(request):
    context = {'username':request.session['username'], 
               'member_type':request.session['member_type']}
    if request.method == 'POST':
        nama_tim = request.POST.get('nama_tim')
        universitas = request.POST.get('universitas')
        username = request.session['username']
        cursor = connection.cursor()
        query = f"""
        select id_manajer
        from user_system U, manajer M
        where m.username = u.username and u.username = '{username}';
        """
        cursor.execute('set search_path to public')
        cursor.execute(query)
        res = parse(cursor)
        manajer = res[0]
        id_manajer = manajer['id_manajer']
        
        query2 = f"""
        INSERT INTO TIM VALUES ('{nama_tim}','{universitas}');
        INSERT INTO TIM_MANAJER VALUES ('{id_manajer}','{nama_tim}');
        """      
        try:
            cursor.execute('set search_path to public')
            cursor.execute(query2)
            return redirect('manageteam:viewTeam')
        except InternalError as e: 
            messages.info(request, str(e.args))
    return render(request, 'daftarTeam.html', context)

def daftarPelatih(request, nama_tim):
    context = {'username':request.session['username'], 
               'member_type':request.session['member_type']}
    cursor = connection.cursor()
    query = f"""
    select nama_depan, nama_belakang, p.id_pelatih as id_pelatih, spesialisasi
    from pelatih P, spesialisasi_pelatih S, non_pemain n
    where nama_tim is null and s.id_pelatih = p.id_pelatih and 
    p.id_pelatih = n.id;
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    print('res ' + str(res))
    coaches = []
    for pelatih in res:
        pelatih_detail = {}
        for attr in pelatih:
            if isinstance(pelatih[attr], uuid.UUID):
                pelatih_detail[attr] = str(pelatih[attr])
            else:
                pelatih_detail[attr] = pelatih[attr]
        coaches.append(pelatih_detail)
    context['coaches'] = coaches
    if request.method == 'POST':
        pelatih_picked = request.POST.get('pelatih_picked')
        cursor = connection.cursor()
        if (pelatih_picked == None):
            response = HttpResponseRedirect(reverse('manageteam:viewTeam'))
            return response
        query = f"""
            UPDATE PELATIH
            SET nama_tim = '{nama_tim}'
            WHERE id_pelatih = '{pelatih_picked}';
        """
        cursor.execute(query)
        response = HttpResponseRedirect(reverse('manageteam:viewTeam'))
        return response
    return render(request, 'daftarPelatih.html', context)

def daftarPemain(request, nama_tim):
    context = {'username':request.session['username'], 
               'member_type':request.session['member_type']}
    cursor = connection.cursor()
    query = f"""
    select nama_depan, nama_belakang, id_pemain, posisi, npm, jenjang
    from pemain
    where nama_tim is null
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    players = []
    for pemain in res:
        pemain_detail = {}
        for attr in pemain:
            if isinstance(pemain[attr], uuid.UUID):
                pemain_detail[attr] = str(pemain[attr])
            else:
                pemain_detail[attr] = pemain[attr]
        players.append(pemain_detail)
    context = {
        'players':players
    }
    if request.method == 'POST':
        pemain_picked = request.POST.get('pemain_picked')
        cursor = connection.cursor()
        if (pemain_picked == None):
            response = HttpResponseRedirect(reverse('manageteam:viewTeam'))
            return response
        query = f"""
            UPDATE PEMAIN 
            SET nama_tim = '{nama_tim}'
            WHERE id_pemain = '{pemain_picked}';
        """
        cursor.execute(query)
        response = HttpResponseRedirect(reverse('manageteam:viewTeam'))
        return response
        
    return render(request, 'daftarPemain.html', context)

def deletePemain(request, id_pemain):
    cursor = connection.cursor()
    query = f"""
    UPDATE PEMAIN
    SET nama_tim = NULL
    WHERE id_pemain = '{id_pemain}';
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    response = HttpResponseRedirect(reverse('manageteam:viewTeam'))
    return response

def deletePelatih(request, id_pelatih):
    cursor = connection.cursor()
    query = f"""
    UPDATE PELATIH
    SET NAMA_TIM = NULL
    WHERE ID_PELATIH = '{id_pelatih}';
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    response = HttpResponseRedirect(reverse('manageteam:viewTeam'))
    return response

def makeCaptainPemain(request, id_pemain, nama_tim):
    cursor = connection.cursor()
    query = f"""
    SELECT id_pemain
    FROM PEMAIN
    WHERE IS_CAPTAIN = TRUE AND NAMA_TIM = '{nama_tim}';
    """
    cursor.execute(query)
    res = parse(cursor)
    if len(res) == 1:
        captain = res[0]
        id_captain = str(captain['id_pemain'])
        query2 = f"""
        UPDATE PEMAIN
        SET is_captain = False
        where id_pemain = '{id_captain}';
        
        UPDATE PEMAIN
        SET is_captain = True
        WHERE id_pemain = '{id_pemain}';
        """
        cursor.execute('set search_path to public')
        cursor.execute(query2)
        response = HttpResponseRedirect(reverse('manageteam:viewTeam'))
        return response
    else:
        query3 = """
        UPDATE PEMAIN
        SET is_captain = True
        WHERE id_pemain = '{id_pemain}';
        """
        cursor.execute('set search_path to public')
        cursor.execute(query3)
        response = HttpResponseRedirect(reverse('manageteam:viewTeam'))
        return response

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]