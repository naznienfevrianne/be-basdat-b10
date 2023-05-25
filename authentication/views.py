from django.shortcuts import render
from authentication.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
import uuid
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import connection, InternalError


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cursor = connection.cursor()
        query = f"""
        SELECT COALESCE(c.username, a.username, m.username) as username,
        CASE
            WHEN c.username IS NOT NULL THEN 'panitia'
            WHEN a.username IS NOT NULL THEN 'penonton'
            WHEN m.username IS NOT NULL THEN 'manajer'
            ELSE 'UNKNOWN'
        END AS MEMBER_TYPE
        FROM USER_SYSTEM as U
        LEFT OUTER JOIN PANITIA AS C on c.username = u.username
        LEFT OUTER JOIN PENONTON AS A on a.username = u.username
        LEFT OUTER JOIN MANAJER AS M on m.username = u.username
        WHERE U.password = '{password}' AND U.username = '{username}';
        """
        cursor.execute('set search_path to public')
        cursor.execute(query)
        res = parse(cursor)
        print("AAAA INI QUERY: " + query)
        print("AAAAAAAAAAAAA INI RES:" + str(res))
        
        if len(res) == 1:
            mem = res[0]
            for attr in mem:
                if isinstance(mem[attr], uuid.UUID):
                    request.session[attr] = str(mem[attr])
                else:
                    request.session[attr] = mem[attr]
            return redirect('dashboard:show_dashboard')
        else:
            messages.info(request, "Username atau password salah")
        
        return render(request, 'login.html')
            
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def registerManajer(request):
    if request.method == 'POST':
        username = request.POST.get('username') # PK
        password = request.POST.get('password') # NOT NULL
        nama_depan = request.POST.get('nama_depan') # NOT NULL
        nama_belakang = request.POST.get('nama_belakang') # NOT NULL
        nomor_hp = request.POST.get('nomor_hp') # NOT NULL
        email = request.POST.get('email') # NOT NULL
        alamat = request.POST.get('alamat') # NOT NULL
        status = '' # masuknya ke status_nn pemain
        id_manajer = uuid.uuid4() #
        if request.POST.get('mahasiswa', None) == 'on':
            status = 'Mahasiswa'
        elif request.POST.get('dosen', None) == 'on':
            status = 'Dosen'
        elif request.POST.get('tendik', None) == 'on':
            status = 'Tendik'
        elif request.POST.get('Alumni', None) == 'on':
            status = 'Alumni'
        elif request.POST.get('Umum', None) == 'on':
            status = 'Umum'
        
        cursor = connection.cursor() 
        query = f"""
        INSERT INTO USER_SYSTEM VALUES ('{username}', '{password}');
        
        INSERT INTO NON_PEMAIN VALUES ('{id_manajer}', '{nama_depan}', '{nama_belakang}', 
        '{nomor_hp}', '{email}', '{alamat}');
        
        INSERT INTO STATUS_NON_PEMAIN VALUES ('{id_manajer}', '{status}');
        
        INSERT INTO MANAJER VALUES ('{id_manajer}', '{username}');
        """   
        print("ini query " + query)
        try:
            cursor.execute('set search_path to public')
            cursor.execute(query)
            return redirect('authentication:login')
        except InternalError as e: 
            messages.info(request, str(e.args))
            
    return render(request, 'registerManajer.html')

def registerPanitia(request):
    if request.method == 'POST':
        username = request.POST.get('username') # PK
        password = request.POST.get('password') # NOT NULL
        nama_depan = request.POST.get('nama_depan') # NOT NULL
        nama_belakang = request.POST.get('nama_belakang') # NOT NULL
        nomor_hp = request.POST.get('nomor_hp') # NOT NULL
        email = request.POST.get('email') # NOT NULL
        alamat = request.POST.get('alamat') # NOT NULL
        jabatan = request.POST.get('jabatan') # NOT NULL
        status = '' # masuknya ke status_nn pemain
        id_panitia = uuid.uuid4() #
        if request.POST.get('mahasiswa', None) == 'on':
            status = 'Mahasiswa'
        elif request.POST.get('dosen', None) == 'on':
            status = 'Dosen'
        elif request.POST.get('tendik', None) == 'on':
            status = 'Tendik'
        elif request.POST.get('Alumni', None) == 'on':
            status = 'Alumni'
        elif request.POST.get('Umum', None) == 'on':
            status = 'Umum'
        
        cursor = connection.cursor() 
        query = f"""
        INSERT INTO USER_SYSTEM VALUES ('{username}', '{password}');
        
        INSERT INTO NON_PEMAIN VALUES ('{id_panitia}', '{nama_depan}', '{nama_belakang}', 
        '{nomor_hp}', '{email}', '{alamat}');
        
        INSERT INTO STATUS_NON_PEMAIN VALUES ('{id_panitia}', '{status}');
        
        INSERT INTO PANITIA VALUES ('{id_panitia}', '{jabatan}', '{username}');
        """   
        print("ini query " + query)
        try:
            cursor.execute('set search_path to public')
            cursor.execute(query)
            return redirect('authentication:login')
        except InternalError as e: 
            messages.info(request, str(e.args))
    return render(request, 'registerPanitia.html')

def registerPenonton(request):
    if request.method == 'POST':
        username = request.POST.get('username') # PK
        password = request.POST.get('password') # NOT NULL
        nama_depan = request.POST.get('nama_depan') # NOT NULL
        nama_belakang = request.POST.get('nama_belakang') # NOT NULL
        nomor_hp = request.POST.get('nomor_hp') # NOT NULL
        email = request.POST.get('email') # NOT NULL
        alamat = request.POST.get('alamat') # NOT NULL
        status = '' # masuknya ke status_nn pemain
        id_penonton = uuid.uuid4() #
        if request.POST.get('mahasiswa', None) == 'on':
            status = 'Mahasiswa'
        elif request.POST.get('dosen', None) == 'on':
            status = 'Dosen'
        elif request.POST.get('tendik', None) == 'on':
            status = 'Tendik'
        elif request.POST.get('Alumni', None) == 'on':
            status = 'Alumni'
        elif request.POST.get('Umum', None) == 'on':
            status = 'Umum'
        
        cursor = connection.cursor() 
        query = f"""
        INSERT INTO USER_SYSTEM VALUES ('{username}', '{password}');
        
        INSERT INTO NON_PEMAIN VALUES ('{id_penonton}', '{nama_depan}', '{nama_belakang}', 
        '{nomor_hp}', '{email}', '{alamat}');
        
        INSERT INTO STATUS_NON_PEMAIN VALUES ('{id_penonton}', '{status}');
        
        INSERT INTO PENONTON VALUES ('{id_penonton}', '{username}');
        """   
        print("ini query " + query)
        try:
            cursor.execute('set search_path to public')
            cursor.execute(query)
            return redirect('authentication:login')
        except InternalError as e: 
            messages.info(request, str(e.args))
    return render(request, 'registerPenonton.html')

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def logout(request):
    request.session['username'] = 'not found'
    request.session['member_type'] = 'not found'
    response = HttpResponseRedirect(reverse('example_app:index'))
    return response