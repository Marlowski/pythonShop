from django.shortcuts import render, redirect

from Cart.models import Cart, add_item
from .forms import CommentForm
from .models import Ring, Comment
from static.script.search import search_script


# Create your views here.

def ring_detail(request, **kwargs):
    ring_id = kwargs['pk']
    that_one_ring = Ring.objects.get(id=ring_id)
    comments = Comment.objects.filter(ring=that_one_ring)

    # Add comment
    if request.method == 'POST':
        # Check if POST req. comes from search form
        if request.POST.__contains__('search_input'):
            return search_script(request)

        if request.POST.__contains__('add_to_cart'):
            add_item(request, that_one_ring)
            return render(request, 'ring-detail.html', context={'that_one_ring': that_one_ring,
                                                                'comments_for_that_one_ring': comments,
                                                                'upvotes': that_one_ring.get_upvotes_count(),
                                                                'downvotes': that_one_ring.get_downvotes_count(),
                                                                'comment_form': CommentForm})
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.ring = that_one_ring
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    # /end if==POST

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


def rings_list(request, **kwargs):
    if request.method == 'POST' and request.POST.__contains__('search_input'):
        # Check if POST req. comes from search form
        return search_script(request)

    product_query = Ring.objects.filter(bezeichnung__contains=kwargs['query'])
    context = {'product_list': product_query, 'query_origin': False, 'query_text': kwargs['query']}

    # view called via search input
    if request.path_info.__contains__("result"):
        context['query_origin'] = True

    return render(request, 'rings-list.html', context)
