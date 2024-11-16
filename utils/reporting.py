from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse

def generar_pdf(data, template_name='reporte.html'):
    """
    Genera un PDF a partir de una plantilla HTML.
    """
    # Renderizar la plantilla HTML con los datos proporcionados
    html_content = render_to_string(template_name, data)

    # Configurar la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    # Manejar errores en la generación del PDF
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response
