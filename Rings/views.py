from django.shortcuts import render, redirect
from Cart.models import add_item
from static.script.search import search_script, search_range_rating
from static.script.utility import create_pdf
from .models import Ring, Rating, RatingEvaluation


def ring_detail(request, **kwargs):
    ring_id = kwargs['pk']
    ring_elem = Ring.objects.get(id=ring_id)

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
                                   'rating': ring_elem.get_rating(),
                                   'rating_amount': ring_elem.get_amount_of_ratings(),
                                   'rating_objects': ring_elem.get_rating_objects(),
                                   'already_rated': check_if_user_rated(request, ring_elem)
                                   })

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
                           'rating': ring_elem.get_rating(),
                           'rating_amount': ring_elem.get_amount_of_ratings(),
                           'rating_objects': ring_elem.get_rating_objects(),
                           'already_rated': True,
                           }
                return render(request, 'ring-detail.html', context)

            # get comment for rating
            comment = request.POST['comment']

            # create new rating (ajax will reload)
            Rating.objects.create(rating=rating, comment=comment, user=request.user, ring=ring_elem)
            context = {'ring_elem': ring_elem,
                       'rating': ring_elem.get_rating(),
                       'rating_amount': ring_elem.get_amount_of_ratings(),
                       'rating_objects': ring_elem.get_rating_objects(),
                       'already_rated': True,
                       }
            return render(request, 'ring-detail.html', context)

        # delete or edit rating handler
        elif request.POST.__contains__('action'):
            action = request.POST['action']
            rating_object = Rating.objects.get(id=request.POST['rating_id'])

            if action == "delete":
                # check if userid matches ratings creator id
                # TODO: also check for role, if admin is trying to delete, let through aswell
                if request.user.id == rating_object.user_id:
                    rating_object.delete()

            elif action == "edit":
                new_text = request.POST['comment']
                if request.user.id == rating_object.user_id:
                    rating_object.comment = new_text
                    rating_object.save()

            elif action == "evaluate":
                evaluation = request.POST['evaluation']
                # check if already evaluated for certain evaluation (cant evaluate as helpful twice)
                existing_ev_amount = 0
                if evaluation != "REP":
                    all_evs = RatingEvaluation.objects.filter(user=request.user)
                    existing_ev_amount = len(all_evs.exclude(evaluation="REP"))

                if existing_ev_amount == 0 and request.user.id is not None:
                    RatingEvaluation.objects.create(evaluation=evaluation, user=request.user, rating=rating_object)

            context = {'ring_elem': ring_elem,
                       'rating': ring_elem.get_rating(),
                       'rating_amount': ring_elem.get_amount_of_ratings(),
                       'rating_objects': ring_elem.get_rating_objects(),
                       'already_rated': check_if_user_rated(request, ring_elem),
                       }
            return render(request, 'ring-detail.html', context)
    # /end if==POST

    context = {'ring_elem': ring_elem,
               'rating': ring_elem.get_rating(),
               'rating_amount': ring_elem.get_amount_of_ratings(),
               'rating_objects': ring_elem.get_rating_objects(),
               'already_rated': check_if_user_rated(request, ring_elem),
               }
    return render(request, 'ring-detail.html', context)


def check_if_user_rated(request, ring_elem):
    if request.user.id is None:
        return False
    return len(Rating.objects.filter(user=request.user, ring=ring_elem)) > 0


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
            product_query = search_range_rating(search_input)
            search_input = search_input + " Sterne"

        elif category == "size":
            product_query = Ring.objects.filter(ring_size__contains=search_input)
            search_input = search_input + " mm"
        else:
            product_query = Ring.objects.filter(bezeichnung__contains=search_input)

        context = {'product_list': product_query, 'query_origin': True, 'query_text': search_input}
        return render(request, 'rings-list.html', context)

    # page called from category
    else:
        product_query = Ring.objects.filter(bezeichnung__contains=kwargs['query'])
        product_query = product_query.order_by("ring_size")
        context = {'product_list': product_query, 'query_origin': False, 'query_text': kwargs['query']}
        return render(request, 'rings-list.html', context)
