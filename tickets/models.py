from django.db import models
from django.conf import settings 
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de la Categoría")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción de la Categoría")

    def __str__(self):
        return self.name

class Type(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="types", verbose_name="Categoría")
    name = models.CharField(max_length=100, verbose_name="Nombre del Tipo")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción del Tipo")

    def __str__(self):
        return self.name

class Priority(models.Model):
    level = models.CharField(max_length=50, verbose_name="Nivel de Prioridad")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción de la Prioridad")

    def __str__(self):
        return f"{self.level} - {self.description}"

class Ticket(models.Model):
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_proceso', 'En Proceso'),
        ('cerrado', 'Cerrado')
    ]

    nombre_solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    servicio = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, related_name="tickets", verbose_name="Servicio")  # Cambio de 'type' a 'Type'
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción del Ticket")
    prioridad = models.ForeignKey('Priority', on_delete=models.SET_NULL, null=True, related_name="tickets", verbose_name="Prioridad")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='abierto', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_solicitante} - {self.prioridad} - {self.estado}"

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments", verbose_name="Ticket")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Usuario")
    content = models.TextField(verbose_name="Contenido del Comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return f"Comentario de {self.user} en {self.ticket}"


from django.db import models

class Feedback(models.Model):
    ticket = models.ForeignKey(
        'Ticket',  # Relación con el modelo Ticket
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    satisfaccion = models.IntegerField(
        choices=[(i, f'{i} - {desc}') for i, desc in enumerate(
            ['Muy insatisfecho', 'Insatisfecho', 'Neutral', 'Satisfecho', 'Muy satisfecho'], start=1
        )],
        verbose_name="Satisfacción"
    )
    comentarios = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comentarios adicionales"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return f"Feedback para Ticket #{self.ticket.id} - {self.get_satisfaccion_display()}"
