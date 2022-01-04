from decimal import Decimal

from django.shortcuts import render, redirect

from static.script.search import search_script
from static.script.utility import get_client_ip
from .models import Cart, CartItem, Payment


# isnt called yet
# TODO: on user log in, check if carts can be merged
def cart_merge(request):
    # error catching
    if request.user.id is None:
        return
    # check if account cart exists
    account_cart = Cart.objects.filter(user_elem=request.user).first()
    # check if ip cart exists as well
    ip_cart = Cart.objects.filter(user_ip=get_client_ip(request), user_elem=None).first()

    # if no cart for user exists yet, but for his ip, create new cart
    if account_cart is None and ip_cart is not None:
        account_cart = Cart.objects.create(user_elem=request.user, user_ip=get_client_ip(request))

    if ip_cart:
        # merge all ip-cart items into account cart, and delete ip-cart
        ip_cart_objects = CartItem.objects.filter(cart_id=ip_cart.id)
        for item in ip_cart_objects:
            # check for same item and if necessary just change quantity
            same_product_existing = CartItem.objects.filter(cart=account_cart, product_id=item.product_id).first()
            if same_product_existing is not None:
                same_product_existing.quantity += 1
                same_product_existing.save()
            else:
                CartItem.objects.create(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    product_img_url=item.product_img_url,
                    price=item.price,
                    quantity=item.quantity,
                    cart=account_cart
                )
            CartItem.objects.filter(id=item.id).delete()
        Cart.objects.filter(id=ip_cart.id).delete()


def change_quantity(request, add):
    if request.user.id is not None:
        cart = Cart.objects.get(user_elem=request.user)
    else:
        cart = Cart.objects.get(user_ip=get_client_ip(request), user_elem=None)

    if cart:
        if add:
            item = CartItem.objects.filter(cart=cart, product_id=request.POST.get('change_quantity_add')).first()
        else:
            item = CartItem.objects.filter(cart=cart, product_id=request.POST.get('change_quantity_rem')).first()
        if item:
            if add:
                item.quantity += 1
                item.save()
            else:
                if item.quantity == 1:
                    item.delete()
                else:
                    item.quantity -= 1
                    item.save()
    return redirect('cart-show')


# Cart can be used by logged in user or non logged in user
# if the cart is used, when not logged in, the cart utilizes the ip-adress of the user
def show_cart(request):
    if request.method == 'POST':
        # Check if POST req. comes from search form
        if request.POST.__contains__('search_input'):
            return search_script(request)

        # user clicked empty btn
        if 'empty' in request.POST:
            if request.user.id is not None:
                Cart.objects.get(user_elem=request.user).delete()
            else:
                Cart.objects.get(user_ip=get_client_ip(request), user_elem=None).delete()
            context = {
                'cart_is_empty': True,
                'cart_items': None,
                'amount': 0.0
            }
            return render(request, 'cart.html', context)

        # user clicked pay btn
        elif 'pay' in request.POST:
            return redirect('cart-pay')

        # add quantity
        elif 'change_quantity_add' in request.POST:
            return change_quantity(request, True)

        # subtract quantity
        elif 'change_quantity_rem' in request.POST:
            return change_quantity(request, False)

        # remove an item
        elif 'remove_item' in request.POST:
            if request.user.id is not None:
                cart = Cart.objects.get(user_elem=request.user)
            else:
                cart = Cart.objects.get(user_ip=get_client_ip(request), user_elem=None)
            CartItem.objects.get(cart=cart, product_id=request.POST.get('remove_item')).delete()
            return redirect('cart-show')

    # GET
    else:
        # declare cart init variables
        cart_is_empty = True
        cart_items = None
        total = Decimal(0.0)

        # get user ip adress
        user_ip = get_client_ip(request)

        # not logged in handler
        if request.user.id is None:
            # check existing carts based on ip but dont query carts that have a user_elem set
            carts = Cart.objects.filter(user_ip=user_ip, user_elem=None)
        else:
            # TODO: remove merge test when implemented at proper position
            cart_merge(request)
            # logged in -> check existing user carts
            carts = Cart.objects.filter(user_elem=request.user)

        # check if cart query was successfull, if so add existing cart values to vars, otherwise keep init values
        if carts:
            cart = carts.first()
            cart_is_empty = len(CartItem.objects.filter(cart=cart)) <= 0
            cart_items = CartItem.objects.filter(cart=cart)
            total = cart.get_total()

        context = {
            'cart_is_empty': cart_is_empty,
            'cart_items': cart_items,
            'total': total
        }
        return render(request, 'cart.html', context)


def pay(request):
    cart_is_empty = True
    paid = False
    amount = 0
    logged_in = False

    if request.method == 'POST':
        # Check if POST req. comes from search form
        if request.POST.__contains__('search_input'):
            return search_script(request)

        # get Cart from user / ip-adress
        if request.user.id is not None:
            cart = Cart.objects.filter(user_elem=request.user).first()
        else:
            cart = Cart.objects.filter(user_ip=get_client_ip(request), user_elem=None).first()

        # safety check
        if cart is None:
            redirect('landing-page')

        # get all cart objects
        paid_items = CartItem.objects.filter(cart=cart)
        # just reference for clerks which id's got bought
        item_string_list = ""
        for item in paid_items:
            item_string_list += "id:" + str(item.product_id) + " qt:" + str(item.quantity) + ", "
        item_string_list = item_string_list[0:-1]

        paid = True
        if request.user.id is None:
            user_elem = None
            email = request.POST['email-field']
        else:
            user_elem = request.user
            email = None

        Payment.objects.create(
            user_elem=user_elem,
            email=email,
            credit_card_number=request.POST['card_nmbr'],
            expiry_date=request.POST['exp_date'],
            items_id=item_string_list,
            amount=cart.get_total(),
        )

        if request.user.id is not None:
            Cart.objects.get(user_elem=request.user).delete()
        else:
            Cart.objects.get(user_ip=get_client_ip(request), user_elem=None).delete()

    # GET
    else:
        # get Cart from user / ip-adress
        if request.user.id is not None:
            logged_in = True
            carts = Cart.objects.filter(user_elem=request.user)
        else:
            carts = Cart.objects.filter(user_ip=get_client_ip(request), user_elem=None)

        if carts:
            cart = carts.first()
            cart_is_empty = len(CartItem.objects.filter(cart=cart)) <= 0
            amount = cart.get_total()

        # if cart is empty redirect only on GET, since after payment the cart gets cleared and shows a success message
        if cart_is_empty:
            return redirect('landing-page')

    context = {
        'cart_is_empty': cart_is_empty,
        'amount': amount,
        'paid': paid,
        'logged_in': logged_in,
    }

    return render(request, 'pay.html', context)
