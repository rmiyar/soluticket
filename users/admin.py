from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff')

    # Agrega un campo para seleccionar el grupo en la interfaz de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'groups'),  # Usa `groups` en lugar de `user_group`
        }),
    )

    def save_model(self, request, obj, form, change):
        # Guarda el usuario en la base de datos
        super().save_model(request, obj, form, change)
        # Agrega el grupo seleccionado si se asignó alguno
        selected_groups = form.cleaned_data.get('groups', [])
        if selected_groups:
            obj.groups.set(selected_groups)  # Asigna el grupo seleccionado

admin.site.register(User, CustomUserAdmin)
