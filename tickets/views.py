from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket,Type,Feedback
from django.shortcuts import render
from .forms import TicketForm,CommentForm,CrearTicketForm
from django.urls import reverse
from django.http import HttpResponse
from utils.decorators import group_required
from django.template.loader import render_to_string
from xhtml2pdf import pisa

@group_required('agente')
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


@group_required('agente')
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


@group_required('agente')
@login_required
def agente_dashboard(request):
    agente = request.user
    tickets_asignados = Ticket.objects.filter(asignado_a=agente)
    
    # Filtrar tickets por estado
    abiertos = tickets_asignados.filter(estado="abierto")
    en_proceso = tickets_asignados.filter(estado="en_proceso")
    cerrados = tickets_asignados.filter(estado="cerrado")
    
    # Instancias de los formularios para el estado y el comentario
    ticket_form = TicketForm()  # Formulario para el campo de estado
    comment_form = CommentForm()  # Formulario para agregar un comentario

    context = {
        "total_tickets": tickets_asignados.count(),
        "abiertos": abiertos,
        "en_proceso": en_proceso,
        "cerrados": cerrados,
        "tickets_asignados": tickets_asignados,
        "ticket_form": ticket_form,
        "comment_form": comment_form,
    }
    
    return render(request, "agente_dashboard.html", context)

@group_required('agente')
@login_required
def editar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, asignado_a=request.user)
    
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=ticket)
        comment_form = CommentForm(request.POST)
        
        if ticket_form.is_valid():
            ticket_form.save()
            
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.user = request.user
                comment.save()
            
            return redirect(reverse("agente_dashboard"))
    else:
        ticket_form = TicketForm(instance=ticket)
        comment_form = CommentForm()
    
    # Asegúrate de pasar los formularios en el contexto para cada modal
    return render(request, "agente_dashboard.html", {
        "ticket_form": ticket_form,
        "comment_form": comment_form,
        "tickets_asignados": Ticket.objects.filter(asignado_a=request.user),
    })




@login_required
@group_required('cliente')
def crear_ticket(request):
    if request.method == 'POST':
        form = CrearTicketForm(request.POST)
        if form.is_valid():
            tipo_name = request.POST.get('tipo_ticket')  # Obtener el nombre del tipo desde el formulario
            if not tipo_name:
                messages.error(request, "Por favor, selecciona un tipo de ticket válido.")
                return redirect('crear_ticket')

            try:
                tipo = Type.objects.get(name=tipo_name)  # Buscar el objeto Type correspondiente
            except Type.DoesNotExist:
                messages.error(request, "El tipo de ticket seleccionado no existe.")
                return redirect('crear_ticket')

            ticket = form.save(commit=False)  # No guardar todavía
            ticket.servicio = tipo  # Asignar el objeto Type al campo 'servicio'
            ticket.nombre_solicitante = request.user  # Asignar el usuario autenticado como dueño
            ticket.save()  # Guardar el ticket con el usuario asignado

            messages.success(request, "El ticket se creó correctamente.")
            return redirect('ver_mis_tickets')  # Cambia a la vista que prefieras tras éxito
        else:
            messages.error(request, "Por favor, corrige los errores del formulario.")
    else:
        form = CrearTicketForm()

    # Separar lógica para obtener tipos por categoría
    tipos_software, tipos_hardware = obtener_tipos_por_categoria()

    return render(request, 'post_ticket.html', {
        'form': form,
        'tipos_software': tipos_software,
        'tipos_hardware': tipos_hardware
    })


def obtener_tipos_por_categoria():
    """Obtiene los tipos de ticket agrupados por categoría."""
    tipos_software = Type.objects.filter(category__name="Software")
    tipos_hardware = Type.objects.filter(category__name="Hardware")
    return tipos_software, tipos_hardware

def generar_pdf_xhtml2pdf(request):
    # Datos para la plantilla
    context = {
        'titulo': 'Reporte de Ejemplo',
        'contenido': 'Este es un reporte generado con xhtml2pdf.',
    }

    # Renderizar la plantilla HTML
    html = render_to_string('reporte.html', context)

    # Crear el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    pisa.CreatePDF(html, dest=response)

    return response

from django.views.generic import ListView
from .models import Ticket

class MisTicketsView( ListView):
    model = Ticket
    template_name = "mis_tickets.html"
    context_object_name = "tickets"

    def get_queryset(self):
        # Filtrar tickets solo para el usuario autenticado
        return Ticket.objects.filter(nombre_solicitante=self.request.user)
    


def dar_feedback(request):
    if request.method == "POST":
        ticket_id = request.POST.get('ticket_id')
        satisfaccion = request.POST.get('satisfaccion')
        comentarios = request.POST.get('comentarios')

        # Validar si el ticket existe
        ticket = get_object_or_404(Ticket, id=ticket_id)

        # Verificar si ya existe un feedback para este ticket
        if Feedback.objects.filter(ticket=ticket).exists():
            messages.error(request, "Ya has enviado un feedback para este ticket.")
            return redirect('ver_mis_tickets')

        # Crear el feedback
        try:
            Feedback.objects.create(
                ticket=ticket,
                satisfaccion=int(satisfaccion),
                comentarios=comentarios
            )
            messages.success(request, "Gracias por tu feedback.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar tu feedback: {e}")
            return redirect('mis_tickets')

    return redirect('mis_tickets')