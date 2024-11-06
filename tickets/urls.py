from django.contrib import admin
from django.urls import path, include
from . import views  
urlpatterns = [

    path('consultar-tickets/', views.consultar_tickets, name='consultar_tickets'),
    path('Tickets/tomar-ticket/<int:ticket_id>/', views.tomar_ticket, name='tomar_ticket'),
    
]
