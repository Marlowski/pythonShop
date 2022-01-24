from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from static.script.search import search_script
from .forms import SignUpForm
from UserManagement.models import MyUser


# TODO: zu funktionsbasierte View ändern um search_input (POST req.) abfragen zu können
class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('landing-page')
    template_name = 'signup.html'


def profile_page(request, **kwargs):
    if request.method == 'POST' and request.POST.__contains__('search_input'):
        # Check if POST req. comes from search form
        return search_script(request)

    user_id = kwargs['pk']
    this_user = MyUser.objects.get(id=user_id)

    if request.method == 'POST':
        if request.POST.__contains__('load_editpage'):
            return redirect('user_profile_edit', pk=user_id)

    context = {'user': this_user}
    return render(request, 'profile-page.html', context)


def profile_edit(request, **kwargs):
    if request.method == 'POST' and request.POST.__contains__('search_input'):
        # Check if POST req. comes from search form
        return search_script(request)

    user_id = kwargs['pk']
    profile = MyUser.objects.get(id=user_id)

    if request.method == 'POST':
        if request.POST.__contains__('discard_changes'):
            return redirect('user_profile')

        print(request.POST)

        if request.POST.__contains__('save_edited_profile'):
            print(request.POST)
            # profile.username = request.POST.get('username', profile.username)
            # profile.email = request.POST.get('email', profile.email)
            profile.profile_picture = request.POST.get('profile_picture', profile.profile_picture)
            profile.save()

    context = {'user': profile}
    return render(request, 'profile-edit.html', context)
