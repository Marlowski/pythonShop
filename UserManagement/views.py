from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm


# TODO: zu funktionsbasierte View ändern um search_input (POST req.) abfragen zu können
class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('landing-page')
    template_name = 'signup.html'
