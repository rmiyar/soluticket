from django.contrib import admin
from .models import Ticket, Type, Priority, Comment

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('nombre_solicitante', 'prioridad', 'estado', 'fecha_creacion', 'servicio')
    list_filter = ('prioridad', 'estado', 'servicio')
    search_fields = ('nombre_solicitante', 'categoria__name', 'prioridad__level')


