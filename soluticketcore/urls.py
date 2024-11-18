from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from .views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  
    path('conocenos/', IndexView.as_view(), name='conocenos'),
     path('', RedirectView.as_view(url='/conocenos/', permanent=True)),  
    path('Tickets/', include('tickets.urls'))
    
]
 