from django.shortcuts import render, redirect

from .forms import CommentForm
from .models import Ring, Comment
from static.script.search import search_script


# Create your views here.

def ring_detail(request, **kwargs):
    print(kwargs)
    ring_id = kwargs['pk']
    that_one_ring = Ring.objects.get(id=ring_id)
    print(str(ring_id), " :: ", that_one_ring)
    context = {'that_one_ring': that_one_ring}

    # Add comment
    if request.method == 'POST':
        # Check if POST req. comes from search form
        if request.POST.__contains__('search_input'):
            return search_script(request)

        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.ring = that_one_ring
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    comments = Comment.objects.filter(ring=that_one_ring)
    context = {'that_one_ring': that_one_ring,
               'comments_for_that_one_ring': comments,
               'upvotes': that_one_ring.get_upvotes_count(),
               'downvotes': that_one_ring.get_downvotes_count(),
               'comment_form': CommentForm}
    return render(request, 'ring-detail.html', context)


def vote(request, pk: str, up_or_down: str):
    ring = Ring.objects.get(id=int(pk))
    user = request.user
    ring.vote(user, up_or_down)
    return redirect('ring_detail', pk=pk)
