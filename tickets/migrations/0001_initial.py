# Generated by Django 5.1.2 on 2024-11-03 21:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre de la Categoría')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción de la Categoría')),
            ],
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=50, verbose_name='Nivel de Prioridad')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción de la Prioridad')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_solicitante', models.CharField(max_length=100, verbose_name='Nombre del Solicitante')),
                ('estado', models.CharField(choices=[('abierto', 'Abierto'), ('en_proceso', 'En Proceso'), ('cerrado', 'Cerrado')], default='abierto', max_length=10, verbose_name='Estado')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('prioridad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='tickets.priority', verbose_name='Prioridad')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Contenido del Comentario')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tickets.ticket', verbose_name='Ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre del Tipo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción del Tipo')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='tickets.category', verbose_name='Categoría')),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='tickets.type', verbose_name='Categoría'),
        ),
    ]
