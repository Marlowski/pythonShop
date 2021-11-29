from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView
from .forms import RingForm
from .models import Ring

# Create your views here.

def ring_detail(request, **kwargs):
    print(kwargs)
    ringID = kwargs['pk']
    thatOneRing = Ring.objects.get(id=ringID)
    print(str(ringID), " :: ", thatOneRing)
    context = {'that_one_ring': thatOneRing}
    return render(request, 'ring-detail.html', context)