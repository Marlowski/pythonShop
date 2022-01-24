from django.http import JsonResponse
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

        # staff or superuser trying to enter edit mode (role handling in other view)
        elif request.POST.__contains__('load_editpage'):
            return redirect('ring-edit', pk=ring_id)

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
                # check if userid matches ratings creator id or if staff or admin is trying to delete/edit
                if request.user.id == rating_object.user_id or \
                        request.user.is_staff == 1 or \
                        request.user.is_superuser == 1:
                    rating_object.delete()

            elif action == "edit":
                new_text = request.POST['comment']
                if request.user.id == rating_object.user_id or \
                        request.user.is_staff == 1 or \
                        request.user.is_superuser == 1:
                    rating_object.comment = new_text
                    rating_object.save()

            elif action == "evaluate":
                evaluation = request.POST['evaluation']
                # check if already evaluated for certain evaluation (cant evaluate as helpful twice)
                # but can always report
                existing_ev_amount = 0
                if evaluation != "REP":
                    all_evs = RatingEvaluation.objects.filter(user=request.user, rating=rating_object.id)
                    existing_ev_amount = len(all_evs.exclude(evaluation="REP"))
                # check if already reported
                else:
                    reports = RatingEvaluation.objects.filter(user=request.user,
                                                              rating=rating_object.id,
                                                              evaluation="REP")
                    existing_ev_amount = len(reports)

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
        product_query = Ring.objects.filter(category__contains=kwargs['query'])
        product_query = product_query.order_by("ring_size")
        context = {'product_list': product_query, 'query_origin': False, 'query_text': kwargs['query']}
        return render(request, 'rings-list.html', context)


def ring_edit(request, **kwargs):
    # handle unauthorized access
    if request.user.is_staff != 1 and request.user.is_superuser != 1:
        return redirect('landing-page')

    if request.method == 'POST' and request.POST.__contains__('search_input'):
        # Check if POST req. comes from search form
        return search_script(request)

    ring_id = kwargs['pk']
    ring_elem = Ring.objects.get(id=ring_id)

    if request.method == 'POST':
        if "discard_changes" in request.POST:
            return redirect('ring_detail', pk=ring_id)

        # delete product
        if request.POST.__contains__('delete_product'):
            Ring.objects.get(id=ring_id).delete()
            return redirect('landing-page')

        # save changes to product
        if request.POST.__contains__("save_edited_product"):
            ring_elem.bezeichnung = request.POST.get('bezeichnung')
            ring_elem.material = request.POST.get('material')
            ring_elem.preis = request.POST.get('preis')
            ring_elem.category = request.POST.get('category')
            ring_elem.ring_size = request.POST.get('size')
            ring_elem.description = request.POST.get('description')
            if request.FILES.get("file") is not None:
                ring_elem.product_img_url = request.FILES.get("file")
            ring_elem.save()
            return JsonResponse({"product_edit": True,
                                 "new_img_url": ring_elem.product_img_url.url,
                                 "new_title": ring_elem.bezeichnung
                                 }, status=200)
    # /end if==POST

    context = {
        'ring_elem': ring_elem,
        'saved': False,
    }

    return render(request, 'product-edit.html', context)
