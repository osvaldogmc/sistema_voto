from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Votante, Voto, Candidato
from django.contrib.auth.decorators import login_required
import sys

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

        if request.method == "POST":
            nombre = request.POST.get("nombre")
            apellido = request.POST.get("apellido")
            rut = request.POST.get("rut")
            correo = request.POST.get("correo")
            candidato = request.POST.get("candidato")
            

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
    except Exception as e:
        print(f'Error en la linea {format(sys.excinfo()[-1].tblineno)} {type(e).__name} {e}')

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
    return render(request, 'candidatos.html', {"candi": candi})

def registrarCandidato(request):
    try:
        nombre = request.POST['txtNombre']
        apellido = request.POST['txtApellido']
        partido = request.POST['txtPartido']

        registro = Candidato.objects.create(nombre=nombre, apellido=apellido, partido=partido)
    except Exception as e:
        print(f'Error en la linea {format(sys.exc_info()[-1].tb_lineno)} {type(e).__name__} {e}')
    return redirect('/candidatos/')


def editarCandidato(request, candidato_id):
    editar = Candidato.objects.get(id=candidato_id)
    return render(request, 'editarCandidato.html', {"editar": editar})

def edicionCandidato(request,candidato_id):
    # id = request.POST['txtId']
    nombre = request.POST['txtNombre']
    apellido = request.POST['txtApellido']
    partido = request.POST['txtPartido']

    editar = Candidato.objects.get(id=candidato_id)
    # editar.id = id
    editar.nombre = nombre
    editar.apellido = apellido
    editar.partido = partido
    editar.save()

    return redirect('/candidatos/')


def eliminarCandidato(request, candidato_id):
    eliminar = Candidato.objects.get(id=candidato_id)
    eliminar.delete()
    return redirect('/candidatos/')