from django.shortcuts import render
from Rings.models import Ring
from Rings.views import ring_detail


def landing_page(request):
    if request.method == 'POST':
        # change request type so next view handles request as GET and not POST
        request.method = 'GET'

        search_input = request.POST['search_input']
        if len(search_input) <= 0:
            return render(request, 'landingpage.html')

        # Check if input is id
        if search_input.isnumeric():
            search_results = Ring.objects.filter(id=int(search_input))
        else:
            search_results = Ring.objects.filter(bezeichnung__contains=search_input)

        # only one elem found
        if len(search_results) == 1:
            return ring_detail(request, pk=search_results[0].id)
        else:
            # TODO: auf List Seite verlinken
            return render(request, 'landingpage.html')
    else:
        # GET request
        return render(request, 'landingpage.html')


def home_page(request):
    return render(request, 'home.html')
