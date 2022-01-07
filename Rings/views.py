from django.shortcuts import render, redirect

from Cart.models import add_item
from static.script.search import search_script
from static.script.utility import create_pdf
from .forms import CommentForm
from .models import Ring, Comment, Rating


def ring_detail(request, **kwargs):
    ring_id = kwargs['pk']
    ring_elem = Ring.objects.get(id=ring_id)
    comments = Comment.objects.filter(ring=ring_elem)

    # Add comment
    if request.method == 'POST':
        # Check if POST req. comes from search form
        if request.POST.__contains__('search_input'):
            return search_script(request)

        if "save_pdf" in request.POST:
            return create_pdf(ring_elem)

        elif "add_to_cart" in request.POST:
            add_item(request, ring_elem)
            return render(request, 'ring-detail.html',
                          context={'ring_elem': ring_elem,
                                   'comments': comments,
                                   'rating': ring_elem.get_rating(),
                                   'rating_amount': ring_elem.get_amount_of_ratings(),
                                   'already_rated': check_if_user_rated(request, ring_elem),
                                   'comment_form': CommentForm})

        # star rating handler
        elif request.POST.__contains__('rating'):
            if request.user.id is None:
                print("Error - non user trying to vote, force login")
                return redirect('login')

            rating = int(request.POST['rating'])
            # make sure rating is in proper range
            if rating < 1 or rating > 5:
                print("Error - rating out of range")
                return redirect('landing-page')

            # check if user already rated
            if check_if_user_rated(request, ring_elem):
                context = {'ring_elem': ring_elem,
                           'comments': comments,
                           'rating': ring_elem.get_rating(),
                           'rating_amount': ring_elem.get_amount_of_ratings(),
                           'already_rated': True,
                           'comment_form': CommentForm}
                return render(request, 'ring-detail.html', context)

            # create new rating (ajax will reload)
            Rating.objects.create(rating=rating, user=request.user, ring=ring_elem)
            context = {'ring_elem': ring_elem,
                       'comments': comments,
                       'rating': ring_elem.get_rating(),
                       'rating_amount': ring_elem.get_amount_of_ratings(),
                       'already_rated': True,
                       'comment_form': CommentForm}
            return render(request, 'ring-detail.html', context)

        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.ring = ring_elem
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    # /end if==POST

    context = {'ring_elem': ring_elem,
               'comments': comments,
               'rating': ring_elem.get_rating(),
               'rating_amount': ring_elem.get_amount_of_ratings(),
               'already_rated': check_if_user_rated(request, ring_elem),
               'comment_form': CommentForm}
    return render(request, 'ring-detail.html', context)


def check_if_user_rated(request, ring_elem):
    if request.user.id is None:
        return False
    return len(Rating.objects.filter(user=request.user, ring=ring_elem)) > 0


def vote(request, pk: str, up_or_down: str):
    ring = Ring.objects.get(id=int(pk))
    user = request.user
    ring.vote(user, up_or_down)
    return redirect('ring_detail', pk=pk)


def rings_list(request, **kwargs):
    if request.method == 'POST' and request.POST.__contains__('search_input'):
        # Check if POST req. comes from search form
        return search_script(request)

    # page called from search
    if request.path_info.__contains__("result"):
        url_data = kwargs['query'].split(":")
        category = url_data[0]
        search_input = url_data[1]

        if category == "rating":
            # TODO: wait for proper rating implementation
            product_query = Ring.objects.filter(bezeichnung__contains=search_input)
        elif category == "desc":
            product_query = Ring.objects.filter(description__contains=search_input)
        else:
            product_query = Ring.objects.filter(bezeichnung__contains=search_input)

        context = {'product_list': product_query, 'query_origin': True, 'query_text': search_input}
        return render(request, 'rings-list.html', context)

    # page called from category
    else:
        product_query = Ring.objects.filter(bezeichnung__contains=kwargs['query'])
        context = {'product_list': product_query, 'query_origin': False, 'query_text': kwargs['query']}
        return render(request, 'rings-list.html', context)
