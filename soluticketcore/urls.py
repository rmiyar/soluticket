from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  
     path('conocenos/', TemplateView.as_view(template_name="index.html"), name='conocenos'),
     path('crear_ticket/', TemplateView.as_view(template_name="post_ticket.html"), name='crear-ticket'),
    
]