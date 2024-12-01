from django.contrib import admin
from .models import Candidato, Votante, Voto

admin.site.register(Candidato)
admin.site.register(Votante)
admin.site.register(Voto)