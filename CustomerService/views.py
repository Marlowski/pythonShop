from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from Rings.forms import RingForm
from Rings.models import Ring
from django.contrib import messages

from static.script.search import search_script


@staff_member_required(login_url='/userManagement/login/')
def start_page(request):
    # Check if POST req. comes from search form
    if request.POST.__contains__('search_input'):
        return search_script(request)

    if request.method == 'POST':
        if 'delete' in request.POST:
            return redirect('product-delete')
        elif 'create' in request.POST:
            return redirect('product-create')
        elif 'list' in request.POST:
            return redirect('list')
    else:
        can_access = False
        myuser = request.user
        if not myuser.is_anonymous:
            can_access = myuser.is_superuser_or_staff()
        context = {'can_access': can_access,
                   }
        return render(request, 'start-page.html', context)


@staff_member_required(login_url='/userManagement/login/')
def product_create(request):
    # Check if POST req. comes from search form
    if request.POST.__contains__('search_input'):
        return search_script(request)

    if request.method == 'POST':
        form = RingForm(request.POST, request.FILES)
        if 'create' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, f"Neues Produkt hinzugefügt: {form.cleaned_data.get('bezeichnung')}")
            else:
                pass
            return redirect('product-create')
    else:
        can_create = False
        myuser = request.user
        form = RingForm()
        if not myuser.is_anonymous:
            can_create = myuser.is_superuser_or_staff()
        context = {'form': form,
                   'can_create': can_create,
                   }
        return render(request, 'product-create.html', context)


@staff_member_required(login_url='/userManagement/login/')
def product_delete(request, pk: str):
    # Check if POST req. comes from search form
    if request.POST.__contains__('search_input'):
        return search_script(request)

    product_id = pk
    if request.method == 'POST':
        if 'delete' in request.POST:
            Ring.objects.get(id=product_id).delete()
            messages.success(request, "Ring erfolgreich gelöscht!")
            return redirect('list')

    else:
        can_delete = False
        myuser = request.user
        if not myuser.is_anonymous:
            can_delete = myuser.is_superuser_or_staff()
        ring = Ring.objects.get(id=product_id)
        context = {'can_delete': can_delete,
                   'product': ring,
                   }
        return render(request, 'product-delete.html', context)


@staff_member_required(login_url='/userManagement/login/')
def product_list(request):
    # Check if POST req. comes from search form
    if request.POST.__contains__('search_input'):
        return search_script(request)

    can_access = False
    myuser = request.user
    if not myuser.is_anonymous:
        can_access = myuser.is_superuser_or_staff()
    all_rings = Ring.objects.all()
    context = {'product_list': all_rings, 'can_access': can_access}
    return render(request, 'rings-list.html', context)

