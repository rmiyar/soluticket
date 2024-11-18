# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Determinar si el usuario pertenece a los grupos "agente" o "cliente"
        context['is_agente'] = user.is_authenticated and user.groups.filter(name="agente").exists()
        context['is_cliente'] = user.is_authenticated and user.groups.filter(name="cliente").exists()
        return context