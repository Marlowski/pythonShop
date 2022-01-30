import io
from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.lib.pagesizes import A4


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_pdf(product_info):
    buffer = io.BytesIO()
    # Create pdf object
    pdf = canvas.Canvas(buffer, pagesize=A4)
    description = product_info.description.replace('. ', '.').split('.')
    image = product_info.product_img_url
    #Background
    pdf.setFillColorRGB(1, 0.9, 0.7)
    pdf.rect(5, 5, 587, 833, fill=1)
    #Description Box
    pdf.setFillColorRGB(1, 1, 1)
    pdf.rect(15, 290, 572, 130, fill=1)
    #Other info Box
    pdf.setFillColorRGB(1, 1, 1)
    pdf.rect(15, 455, 325, 110, fill=1)

    if product_info.material == 'GG':
        material = 'Gelbgold'
    elif product_info.material == 'WG':
        material = 'Weißgold'
    elif product_info.material == 'RG':
        material = 'Roségold'

    textLines = [
        'Artikelnummer: ' + str(product_info.id),
        'Preis: ' + str(product_info.preis) + ' €',
        'Material: ' + material,
        'Kategorie: ' + product_info.category,
        'Ringbreite: ' + product_info.ring_size,
    ]
    pdf.setFont("Courier-Bold", 24)
    pdf.setFillColorRGB(0.8, 0.2, 0.2)
    pdf.setTitle(product_info.bezeichnung + '_Infomaterial')
    pdf.drawCentredString(300, 770, product_info.bezeichnung)

    text = pdf.beginText(40, 540)
    text.setFont("Courier", 14)
    for line in textLines:
        text.textLine(line)
        pdf.setFont("Courier-Bold", 18)

    pdf.drawCentredString(300, 390, 'Beschreibung: ')
    text2 = pdf.beginText(30, 350)
    for line in description:
        text2.textLine(line)
    pdf.drawText(text)
    pdf.drawText(text2)

    pdf.drawImage('.'+image.url, 200, 585, width=(2.5 * inch), height=(2.4 * inch))
    # Close pdf stream
    pdf.showPage()
    pdf.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=product_info.bezeichnung + '.pdf')
