# Generated by Django 5.1.2 on 2024-11-15 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_alter_ticket_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción del Ticket'),
        ),
    ]
