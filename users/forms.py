from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User

class CustomUserCreationForm(UserCreationForm):
    user_group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['cliente', 'agente', 'Administrador']),
        required=True,
        label="Tipo de Usuario"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'user_group')

    def save(self, commit=True):
        # Guarda el usuario sin el grupo aún para asegurarse de que esté en la base de datos
        user = super().save(commit=False)
        if commit:
            user.save()  # Guarda el usuario en la base de datos primero
            # Asigna el grupo seleccionado
            selected_group = self.cleaned_data['user_group']
            user.groups.add(selected_group)  # Agrega el grupo seleccionado al usuario
        return user
