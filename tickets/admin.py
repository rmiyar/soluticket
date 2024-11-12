from django.contrib import admin
from .models import Ticket, Type, Priority, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Número de comentarios adicionales en blanco
    readonly_fields = ('user', 'content', 'created_at')  # Hacer los campos solo de lectura

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('nombre_solicitante', 'prioridad', 'estado', 'fecha_creacion', 'servicio')
    list_filter = ('prioridad', 'estado', 'servicio')
    search_fields = ('nombre_solicitante', 'servicio__name', 'prioridad__level')
    inlines = [CommentInline]  # Agregar los comentarios en línea en la página del ticket

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Ajusta esto según los campos de Type

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('level',)  # Ajusta esto según los campos de Priority

