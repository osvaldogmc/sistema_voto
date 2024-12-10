from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import sys
import re
from .models import Votante, Voto, Candidato
from .functions import encode, decode


def home(request):
    return render(request, 'index.html')


def formulario_votacion(request):
    try:
        context = {'candidatos': []}
        candidatos = Candidato.objects.all()
        if candidatos:
            for candidato in candidatos:
                context['candidatos'].append({
                    'id': candidato.id,
                    'nombre': f'{candidato.nombre} {candidato.apellido}',
                })

        if request.method == "GET":
            return redirect('home')
        
        if request.method == "POST":
            nombre = request.POST.get("nombre")
            apellido = request.POST.get("apellido")
            rut = request.POST.get("txtRut")
            correo = request.POST.get("correo")
            candidato = request.POST.get("candidato")

            if not validar_rut(str(rut)):
                context['tipo'] = 'error'
                context['mensaje'] = 'RUT inválido'
                return render(request, 'formulario_votacion.html', context)
            
            context['rut'] = rut

        #    Valida que el votante exista, y si no existe lo crea
            if Votante.objects.filter(rut=rut).exists():
                votante = Votante.objects.filter(rut=rut).first()
            else:
                votante = Votante(rut=rut, nombre=nombre, correo=correo, apellido=apellido)
                votante.save()
            
        #   Valida que el votante no haya votado
            if Voto.objects.filter(votante=votante).exists():
                context['tipo'] = 'error'
                context['mensaje'] = 'El votante ya votó'
            else:
                voto = Voto(
                    votante = votante,
                    candidato = Candidato(candidato)
                )
                voto.save()
                context['tipo'] = 'succes'
                context['mensaje'] = f'El votante {votante.nombre} {votante.apellido} voto con exito!'

        return render(request, 'formulario_votacion.html', context)
    except IntegrityError:
        return render(request, 'formulario_votacion.html', context)
    

def validar_rut(rut: str):
    rut = rut.replace(".", "").replace("-", "")  # Eliminar puntos y guion
    if not re.match(r'^\d{7,8}[0-9Kk]$', rut):  # Verifica si el formato es correcto
        return False

    cuerpo = rut[:-1]
    dv = rut[-1].upper()  # Convertir el DV a mayúscula

    suma = 0
    multiplicador = 2
    for i in reversed(cuerpo):
        suma += int(i) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2

    dv_calculado = 11 - (suma % 11)
    if dv_calculado == 11:
        dv_correcto = "0"
    elif dv_calculado == 10:
        dv_correcto = "K"
    else:
        dv_correcto = str(dv_calculado)

    return dv == dv_correcto

@login_required
def resultados(request):
    context = {'candidatos': []}
    candidatos = Candidato.objects.all()
    if candidatos:
        for candidato in candidatos:
            contador = Voto.objects.filter(candidato=candidato).count()
            context['candidatos'].append({
                'nombre_candidato': f'{candidato.nombre} {candidato.apellido}',
                'cantidad': contador,
            })
    return render(request, 'resultado.html', context)

def signup(request):
    if request.method == 'GET':
        return render(request, 'admin.html', {
            'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST
                    ['password1'])
                user.save()
                login(request, user)
                return redirect('resultado')
            except IntegrityError:
                return render(request, 'admin.html',{
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'
                })
        return render(request, 'admin.html', {
            'form': UserCreationForm,
            'error': 'La contraseña no coincide'
        })


def ingreso(request):
    if request.method == 'GET':
        return render(request, 'ingreso.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'ingreso.html', {
            'form': AuthenticationForm,
            'error': 'El usuario o contraseña son incorrectos'
        })
        else:
            login(request, user)
            return redirect('resultado')

def signout(request):
    logout(request)
    return redirect('ingreso')


@login_required
def editCandidatos(request):
    candi = Candidato.objects.all()
    candidatos = []
    for c in candi:
        candidatos.append({
           'id': encode(str(c.id)),
            'nombre': c.nombre,
            'apellido': c.apellido,
            'partido': c.partido,
        })
    return render(request, 'candidatos.html', {"candi": candidatos})


def registrarCandidato(request):
    try:
        nombre = request.POST['txtNombre']
        apellido = request.POST['txtApellido']
        partido = request.POST['txtPartido']

        registro = Candidato.objects.create(nombre=nombre, apellido=apellido, partido=partido)
    except Exception as e:
        print(f'Error en la linea {format(sys.exc_info()[-1].tb_lineno)} {type(e).__name__} {e}')
    return redirect('/candidatos/')

@login_required
def editarCandidato(request, candidato_id):
    try:
        id = int(decode(candidato_id))
        candidato = Candidato.objects.get(id=id)

        if Voto.objects.filter(candidato=candidato).exists():
            return redirect('/candidatos/', {'mensaje': 'No se puede editar este candidato porque ya ha recibido votos.'})
        
        candidato_data = {
            'id': encode(str(candidato.id)),
            'nombre': candidato.nombre,
            'apellido': candidato.apellido,
            'partido': candidato.partido,
        }

        return render(request, 'editarCandidato.html', {"editar": candidato_data})
    except Candidato.DoesNotExist:
        return redirect('/candidatos/', {'mensaje': 'Candidato no encontrado.'})

login_required
def edicionCandidato(request):
    id = int(decode(request.POST['txtId']))
    nombre = request.POST['txtNombre']
    apellido = request.POST['txtApellido']
    partido = request.POST['txtPartido']

    editar = Candidato.objects.get(id=id)
    editar.nombre = nombre
    editar.apellido = apellido
    editar.partido = partido
    editar.save()

    return redirect('/candidatos/')

@login_required
def eliminarCandidato(request, candidato_id):
    try:
        id = int(decode(candidato_id))
        candidato = Candidato.objects.get(id=id)

        if Voto.objects.filter(candidato=candidato).exists():
            return redirect('/candidatos/', {'mensaje': 'No se puede eliminar, el candidato ya ha recibido votos!'})


        candidato.delete()
        return redirect('/candidatos/')

    except Candidato.DoesNotExist:
        return redirect('/candidatos/', {'mensaje': 'Candidato no encontrado.'})

