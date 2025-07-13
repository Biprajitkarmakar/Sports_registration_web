from django.template.loader import get_template
from weasyprint import HTML
from django.conf import settings
import os

def generate_pdf(student, request):
    # Convert sports string to list
    sports_list = [s.strip() for s in student.sports.split(',')] if student.sports else []

    template_path = 'myapp/student_pdf.html'
    context = {
        'student': student,
        'MEDIA_URL': settings.MEDIA_URL,
        'sports_list': sports_list
    }

    html_string = get_template(template_path).render(context)
    pdf_bytes = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()

    return pdf_bytes

