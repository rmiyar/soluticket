from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket
from users.models import User
from django.shortcuts import render


def consultar_tickets(request):
    # Obtiene los valores de los filtros
    filtro_servicio = request.GET.get('tipo_servicio', '')
    filtro_prioridad = request.GET.get('prioridad', '')
    filtro_estado = request.GET.get('estado', '')
    filtro_asignado_a = request.GET.get('asignado_a', '')

    # Obtiene todos los tickets inicialmente
    tickets = Ticket.objects.all()

    # Filtra por servicio si el usuario selecciona una opción
    if filtro_servicio:
        tickets = tickets.filter(servicio=filtro_servicio)

    # Filtra por prioridad si el usuario selecciona una opción
    if filtro_prioridad:
        tickets = tickets.filter(prioridad=filtro_prioridad)

    # Filtra por estado si el usuario selecciona una opción
    if filtro_estado:
        tickets = tickets.filter(estado=filtro_estado)

    # Filtra por asignado_a si el usuario ingresa un nombre de usuario
    if filtro_asignado_a:
        tickets = tickets.filter(asignado_a__username=filtro_asignado_a)  # Puedes ajustar para usar ID si es necesario

    # Pasa los tickets filtrados y los valores de los filtros al contexto
    context = {
        'tickets': tickets,
        'tipo_servicio': filtro_servicio,
        'prioridad': filtro_prioridad,
        'estado': filtro_estado,
        'asignado_a': filtro_asignado_a,
    }

    return render(request, 'get_tickets.html', context)


@login_required
def tomar_ticket(request, ticket_id):
    print("Ticket ID:", ticket_id)  # Agrega esta línea para verificar el ID en la consola
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.asignado_a:
        messages.warning(request, "Este ticket ya ha sido tomado por otro usuario.")
    else:
        ticket.asignado_a = request.user
        ticket.estado = 'en_proceso'
        ticket.save()
        messages.success(request, "Has tomado el ticket exitosamente.")

    tickets = Ticket.objects.all()
    return render(request, 'get_tickets.html', {'tickets': tickets})