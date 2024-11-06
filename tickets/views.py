from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket


def consultar_tickets(request):
    # Obtiene los valores de los filtros
    filtro_prioridad = request.GET.get('filtro_prioridad', '')
    filtro_estado = request.GET.get('filtro_estado', '')

    # Obtiene todos los tickets inicialmente
    tickets = Ticket.objects.all()

    # Filtra por prioridad si el usuario selecciona una opción
    if filtro_prioridad:
        tickets = tickets.filter(prioridad=filtro_prioridad)

    # Filtra por estado si el usuario selecciona una opción
    if filtro_estado:
        tickets = tickets.filter(estado=filtro_estado)

    # Pasa los tickets filtrados y los valores de los filtros al contexto
    context = {
        'tickets': tickets,
        'filtro_prioridad': filtro_prioridad,
        'filtro_estado': filtro_estado,
    }

    return render(request, 'get_tickets.html', context)


@login_required
def tomar_ticket(request, ticket_id):
    # Obtener el ticket o lanzar un 404 si no existe
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Verificar si el ticket ya fue tomado
    if ticket.asignado_a:
        messages.warning(request, "Este ticket ya ha sido tomado por otro usuario.")
        return redirect('ruta_lista_tickets')

    # Asignar el ticket al usuario actual y cambiar el estado
    ticket.asignado_a = request.user
    ticket.estado = 'en_proceso'
    ticket.save()

    # Mensaje de éxito y redireccionar a la lista de tickets
    messages.success(request, "Has tomado el ticket exitosamente.")
    return redirect('ruta_lista_tickets')