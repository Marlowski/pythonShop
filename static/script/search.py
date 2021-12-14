from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from Rings.models import Ring


def search_script(request):
    if request.method == 'POST':
        # change request type so next view handles request as GET and not POST
        request.method = 'GET'

        search_input = request.POST['search_input']
        if len(search_input) <= 0:
            return HttpResponseRedirect(request.path_info)

        # Check if input is id
        if search_input.isnumeric():
            search_results = Ring.objects.filter(id=int(search_input))
        else:
            search_results = Ring.objects.filter(bezeichnung__contains=search_input)

        # only one elem found
        if len(search_results) == 1:
            return redirect('/rings/product/' + str(search_results[0].id))
        else:
            return redirect('/rings/list/results/' + search_input)
