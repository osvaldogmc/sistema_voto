from django.db import models

class Candidato(models.Model):
    id = models.AutoField(primary_key= True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Candidato")
    apellido = models.CharField(max_length=100, verbose_name="Apellido del Candidato")
    partido = models.CharField(max_length=100, verbose_name="Partido Político")

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.partido})"


class Votante(models.Model):
    id = models.AutoField(primary_key= True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Votante")
    apellido = models.CharField(max_length=100, verbose_name="Apellido del Votante")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT del Votante")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"


class Voto(models.Model):
    id = models.AutoField(primary_key= True)
    votante = models.OneToOneField(Votante, on_delete=models.CASCADE, verbose_name="Votante")
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, verbose_name="Candidato Votado")

    def __str__(self):
        return f"Voto de {self.votante} para {self.candidato}"
