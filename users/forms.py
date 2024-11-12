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
        user = super().save(commit=False)
        if commit:
            user.save()  # Guarda el usuario en la base de datos
            user.groups.add(self.cleaned_data['user_group'])  # Agrega el grupo seleccionado
        return user
