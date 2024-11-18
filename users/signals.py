from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(user_signed_up)
def assign_client_group(sender, request, user, **kwargs):
    # Obtén el grupo "Cliente", o créalo si no existe
    client_group, created = Group.objects.get_or_create(name="cliente")
    # Asigna el grupo "Cliente" al usuario recién registrado
    user.groups.add(client_group)
