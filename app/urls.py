from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('formulario/', views.formulario_votacion, name='formulario'),
    path('signup/', views.signup, name='signup'),
    path('resultados/', views.resultados, name='resultado'),
    path('ingreso/', views.ingreso, name='ingreso'),
    path('signout/', views.signout, name='signout'),
    path('candidatos/', views.editCandidatos, name='candidatos'),
    path('registrarCandidato/', views.registrarCandidato),
    path('editarCandidato/<candidato_id>', views.editarCandidato, name='editarCandidato'),
    path('edicionCandidato/', views.edicionCandidato),
    path('eliminarCandidato/<candidato_id>', views.eliminarCandidato),
]
