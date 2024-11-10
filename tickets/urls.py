from django.contrib import admin
from django.urls import path, include
from . import views  
from django.views.generic import TemplateView

urlpatterns = [

    path('consultar-tickets/', views.consultar_tickets, name='consultar_tickets'),
    path('crear_ticket/', TemplateView.as_view(template_name="post_ticket.html"), name='crear-ticket'),
    path('Tickets/tomar-ticket/<int:ticket_id>/', views.tomar_ticket, name='tomar_ticket'),
    path("dashboard/agente/", views.agente_dashboard, name="agente_dashboard"),
    path("editar-ticket/<int:ticket_id>/", views.editar_ticket, name="editar_ticket"),
    
]
