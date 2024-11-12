from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(group_name):
    """Verifica si el usuario pertenece a un grupo específico."""
    def in_group(user):
        if user.groups.filter(name=group_name).exists() or user.is_superuser:
            return True
        raise PermissionDenied  # Opcionalmente puedes redirigir a otra URL
    return user_passes_test(in_group)
