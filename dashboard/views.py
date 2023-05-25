from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection, InternalError
import datetime
# Create your views here.
def dashboard(request):
    if request.session['member_type']== 'manajer':
        username = request.session['username']
        # nama depan, nama belakang, nomor hp, 
        # email, alamat, status
        cursor = connection.cursor()
        query = f"""
        SELECT nama_depan, nama_belakang, nomor_hp, 
        email, alamat, status
        FROM non_pemain N, manajer M, status_non_pemain s
        WHERE m.username = '{username}' and m.id_manajer = n.id
        and n.id = id_non_pemain
        ;"""
        cursor.execute('set search_path to public')
        cursor.execute(query)
        res = parse(cursor)
        context = {'member_type':'manajer'}
        if len(res) == 1:
            mem = res[0]
            for attr in mem:
                context[attr] = mem[attr]
        query2 = f"""
        select t.nama_tim, t.universitas
        from tim as T, manajer as M, tim_manajer as TM
        where tm.id_manajer = m.id_manajer and t.nama_tim = tm.nama_tim 
        and m.username = '{username}';
        """
        cursor.execute(query2)
        res = parse(cursor)
        team = []
        tim_detail = {}
        for tim in res:
            for attr in tim:
                tim_detail[attr] = tim[attr]
            team.append(tim_detail)
        context['team'] = team 
        if(len(team) == 0):
            context['team'] = 'Not exist'
        return render(request, 'dashboardManajer.html', context)
    elif request.session['member_type'] == 'panitia':  
        username = request.session['username']
        # nama depan, nama belakang, nomor hp, 
        # email, alamat, status
        cursor = connection.cursor()
        query = f"""
        SELECT nama_depan, nama_belakang, nomor_hp, 
        email, alamat, status, jabatan
        FROM non_pemain N, panitia C, status_non_pemain s
        WHERE c.username = '{username}' and c.id_panitia = n.id
        and n.id = id_non_pemain
        ;"""
        cursor.execute('set search_path to public')
        cursor.execute(query)
        res = parse(cursor)
        context = {'member_type':'panitia'}
        if len(res) == 1:
            mem = res[0]
            for attr in mem:
                context[attr] = mem[attr] 
        query2 = f"""
        SELECT r.datetime, na.nama_depan as nama_depan_a, na.nama_belakang as nama_belakang_a, r.isi_rapat,
        nb.nama_depan as nama_depan_b, nb.nama_belakang as nama_belakang_b
        FROM RAPAT as R, PANITIA as P, MANAJER A, MANAJER B, NON_PEMAIN NA, NON_PEMAIN NB
        where p.username = '{username}' and p.id_panitia = r.perwakilan_panitia and
        a.id_manajer = r.manajer_tim_a and b.id_manajer = r.manajer_tim_b and
        a.id_manajer = na.id and nb.id = b.id_manajer
        and r.datetime >= CURRENT_TIMESTAMP;
        """
        print("queryku " + query2)
        cursor.execute(query2)
        res = parse(cursor)
        meeting = []
        rapat_detail = {}
        for rapat in res:
            for attr in rapat:
                if isinstance(rapat[attr], datetime.date):
                    formatted_date = rapat[attr].strftime("%d-%m-%Y %H:%M:%S")
                    rapat_detail[attr] = formatted_date
                else:
                    rapat_detail[attr] = rapat[attr]
            meeting.append(rapat_detail)
        context['rapat'] = meeting
        if(len(meeting) == 0):
            context['rapat'] = 'Not exist'
        return render(request, 'dashboardPanitia.html', context)
    elif request.session['member_type'] == 'penonton':
        username = request.session['username']
        # nama depan, nama belakang, nomor hp, 
        # email, alamat, status
        cursor = connection.cursor()
        query = f"""
        SELECT nama_depan, nama_belakang, nomor_hp, 
        email, alamat, status
        FROM non_pemain N, penonton A, status_non_pemain s
        WHERE a.username = '{username}' and a.id_penonton = n.id
        and n.id = id_non_pemain
        ;"""
        cursor.execute('set search_path to public')
        cursor.execute(query)
        res = parse(cursor)
        context = {'member_type':'penonton'}
        if len(res) == 1:
            mem = res[0]
            for attr in mem:
                context[attr] = mem[attr]
        query2 = f"""
        SELECT p.start_datetime, p.end_datetime, s.nama
        FROM pembelian_tiket T, pertandingan P, stadium S, penonton a
        WHERE p.start_datetime >= CURRENT_TIMESTAMP
        AND t.id_penonton = a.id_penonton and a.username = '{username}' 
        AND t.id_pertandingan = p.id_pertandingan
        AND p.stadium = s.id_stadium;
        """
        print("queryku " + query2)
        cursor.execute(query2)
        res = parse(cursor)
        match = []
        pertandingan_detail = {}
        for pertandingan in res:
            for attr in pertandingan:
                if isinstance(pertandingan[attr], datetime.date):
                    formatted_date = pertandingan[attr].strftime("%d-%m-%Y %H:%M:%S")
                    pertandingan_detail[attr] = formatted_date
                else:
                    pertandingan_detail[attr] = pertandingan[attr]
            match.append(pertandingan_detail)
        context['pertandingan'] = match
        if(len(match) == 0):
            context['pertandingan'] = 'Not exist'
        print('context2ku ' + str(context))
        return render(request, 'dashboardPenonton.html', context)

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]