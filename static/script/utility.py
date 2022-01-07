import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_pdf(product_info):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create pdf object
    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 100, "Test")

    # Close pdf stream
    pdf.showPage()
    pdf.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
