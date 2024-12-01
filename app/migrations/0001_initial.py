# Generated by Django 5.1.3 on 2024-11-30 21:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Candidato')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellido del Candidato')),
                ('partido', models.CharField(max_length=100, verbose_name='Partido Político')),
            ],
        ),
        migrations.CreateModel(
            name='Votante',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Votante')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellido del Votante')),
                ('rut', models.CharField(max_length=12, unique=True, verbose_name='RUT del Votante')),
                ('correo', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
            ],
        ),
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.candidato', verbose_name='Candidato Votado')),
                ('votante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.votante', verbose_name='Votante')),
            ],
        ),
    ]
