from django.shortcuts import render
from .models import Ring


# Create your views here.

def ring_detail(request, **kwargs):
    print(kwargs)
    ring_id = kwargs['pk']
    that_one_ring = Ring.objects.get(id=ring_id)
    print(str(ring_id), " :: ", that_one_ring)
    context = {'that_one_ring': that_one_ring}
    return render(request, 'ring-detail.html', context)
