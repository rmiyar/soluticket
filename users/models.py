from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('cliente', 'Cliente'),
        ('agente', 'Agente'),
        ('administrador', 'Administrador'),
    ]

    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='cliente', verbose_name="Tipo de Usuario")

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
