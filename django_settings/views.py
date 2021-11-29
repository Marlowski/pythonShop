from django.shortcuts import render


def landing_page(request):
    return render(request, 'landingpage.html')


def home_page(request):
    return render(request, 'home.html')
