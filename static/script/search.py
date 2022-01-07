import re
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
            search_results = search_range_rating(search_input)

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


def search_range_rating(search_input):
    ring_list = Ring.objects.all()
    matching_items = []

    # range search e.g. 2-4 -> return all rings rated between (including) 2 and 4 stars
    if re.search("[0-4]-[1-5]", search_input):
        min_value = int(search_input.split("-")[0])
        max_value = int(search_input.split("-")[1])

        for ring in ring_list:
            if min_value <= ring.get_rating() <= max_value:
                matching_items.append(ring)

    else:
        # single value search
        for ring in ring_list:
            if ring.get_rating() == int(search_input):
                matching_items.append(ring)

    return matching_items
