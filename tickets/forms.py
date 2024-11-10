# forms.py

from django import forms
from .models import Ticket,Comment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['estado']  # Solo incluir el campo 'estado'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [
            ('en_proceso', 'En Proceso'),
            ('cerrado', 'Cerrado')
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Solo el campo 'content' para agregar un comentario
        labels = {
            'content': 'Comentario'
        }