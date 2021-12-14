from django.shortcuts import render
from static.script.search import search_script


def landing_page(request):
    if request.method == 'POST' and request.POST.__contains__('search_input'):
        # Check if POST req. comes from search form
        return search_script(request)
    else:
        return render(request, 'landingpage.html')


def home_page(request):
    return render(request, 'home.html')
