from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic


# TODO: zu funktionsbasierte View ändern um search_input (POST req.) abfragen zu können
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('landing-page')
    template_name = 'signup.html'
