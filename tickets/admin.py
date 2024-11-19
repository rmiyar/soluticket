from django.contrib import admin
from .models import Ticket, Type, Priority, Comment,Feedback
from django.http import HttpResponse
from utils.reporting import generar_pdf



@admin.action(description="Generar reporte en PDF")
def generar_reporte_pdf(modeladmin, request, queryset):
    """
    Acción personalizada para generar un reporte PDF desde el admin.
    """
    # Optimizar la consulta para incluir datos relacionados de servicio y prioridad
    tickets = queryset.select_related('servicio', 'prioridad').values(
        'id',
        'nombre_solicitante',
        'servicio__name',  # Acceder al campo `name` del servicio
        'prioridad__description',  # Acceder al campo `description` de la prioridad
        'estado',
        'fecha_creacion'
    )

    # Preparar el contexto para la plantilla
    data = {
        'titulo': 'Reporte de Tickets',
        'tickets': tickets,  # Asegúrate de que contiene los datos correctos
    }


    return generar_pdf(data, template_name='reporte.html')


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Número de comentarios adicionales en blanco
    readonly_fields = ('user', 'content', 'created_at')  # Hacer los campos solo de lectura


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0  # No mostrar filas en blanco adicionales
    readonly_fields = ('satisfaccion', 'comentarios', 'fecha_creacion')  # Solo lectura
    can_delete = False  # Evitar que se borren desde el Inline   

# Admin del modelo Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_solicitante', 'servicio', 'prioridad', 'estado', 'fecha_creacion')
    list_filter = ('prioridad', 'estado', 'servicio')
    search_fields = ('nombre_solicitante', 'servicio__name', 'prioridad__level')
    inlines = [CommentInline, FeedbackInline]  # Agregar los comentarios en línea en la página del ticket
    actions = [generar_reporte_pdf]  # Registrar la acción personalizada

# Admin del modelo Type
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Ajusta esto según los campos de Type

# Admin del modelo Priority
@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('level',)  # Ajusta esto según los campos de Priority


