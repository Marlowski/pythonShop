from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from Rings.models import Ring


def search_script(request):
    if request.method == 'POST':
        # change request type so next view handles request as GET and not POST
        request.method = 'GET'

        search_input = request.POST['search_input']
        search_type = request.POST['search-type']

        # handle invalid input
        if len(search_input) <= 0 or search_type == "info":
            return HttpResponseRedirect(request.path_info)

        if search_type == "desc":
            search_results = Ring.objects.filter(description__contains=search_input)

        elif search_type == "rating":
            # TODO: wait for proper rating implementation
            search_results = Ring.objects.filter(Ring.objects.get_average_upvote() == search_input)

        # search by name, id (default)
        else:
            # Check if input is id
            if search_input.isnumeric():
                search_results = Ring.objects.filter(id=int(search_input))
                # try name search if query doesnt yield any results
                if len(search_results) == 0:
                    search_results = Ring.objects.filter(bezeichnung__contains=search_input)
            else:
                search_results = Ring.objects.filter(bezeichnung__contains=search_input)

        # only one elem found
        if len(search_results) == 1:
            return redirect('/rings/product/' + str(search_results[0].id))
        else:
            return redirect('/rings/list/results/' + search_type + ":" + search_input)
