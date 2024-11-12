from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  
    path('conocenos/', TemplateView.as_view(template_name="index.html"), name='conocenos'),
     path('', RedirectView.as_view(url='/conocenos/', permanent=True)),  
    path('Tickets/', include('tickets.urls'))
    
]
 