# urls.py
from django.urls import path
from .views import crear_ticket, consultar_tickets, tomar_ticket, agente_dashboard, editar_ticket

urlpatterns = [
    path('crear-ticket/', crear_ticket, name='crear_ticket'),
    path('consultar-tickets/', consultar_tickets, name='consultar_tickets'),
    path('tomar-ticket/<int:ticket_id>/', tomar_ticket, name='tomar_ticket'),
    path('agente-dashboard/', agente_dashboard, name='agente_dashboard'),
    path('editar-ticket/<int:ticket_id>/', editar_ticket, name='editar_ticket'),
]
