from decimal import Decimal

from django.shortcuts import render, redirect

from static.script.search import search_script
from static.script.utility import get_client_ip
from .models import Cart, CartItem


# isnt called yet
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
            CartItem.objects.create(
                product_id=item.product_id,
                product_name=item.product_name,
                price=item.price,
                quantity=item.quantity,
                cart=account_cart
            )
            CartItem.objects.filter(id=item.id).delete()
        Cart.objects.filter(id=ip_cart.id).delete()


# Cart can be used by logged in user or non logged in user
# if the cart is used, when not logged in, the cart utilizes the ip-adress of the user
# TODO: on user log in, check if carts can be merged
def show_cart(request):
    if request.method == 'POST':
        # Check if POST req. comes from search form
        if request.POST.__contains__('search_input'):
            return search_script(request)

        # user clicked empty btn
        if 'empty' in request.POST:
            Cart.objects.get(user_elem=request.user).delete()
            context = {
                'cart_is_empty': True,
                'cart_items': None,
                'amount': 0.0
            }
            return render(request, 'cart.html', context)

        # user clicked pay btn
        elif 'pay' in request.POST:
            return redirect('cart-pay')
    # GET
    else:
        cart_merge(request)
        # declare cart init variables
        cart_is_empty = True
        cart_items = None
        total = Decimal(0.0)

        # get user ip adress
        user_ip = get_client_ip(request)

        # not logged in handler
        if request.user.id is None:
            # check existing carts based on ip
            carts = Cart.objects.filter(user_ip=user_ip)
        else:
            # logged in -> check existing user carts
            carts = Cart.objects.filter(user_elem=request.user)

        # check if cart query was successfull, if so add existing cart values to vars, otherwise keep init values
        if carts:
            cart = carts.first()
            cart_is_empty = False
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
    form = None

    if request.method == 'POST':
        # Check if POST req. comes from search form
        if request.POST.__contains__('search_input'):
            return search_script(request)

        user_elem = request.user
        # 1:00:12 Cart
        paid = True
        Cart.objects.get(user_elem=user_elem).delete()

    else:
        carts = Cart.objects.filter(user_elem=request.user)
        if carts:
            cart = carts.first()
            cart_is_empty = False
            # form = PaymentForm(initial={'amount': cart.get_total()})

    context = {
        'cart_is_empty': cart_is_empty,
        'payment_form': form,
        'paid': paid,
    }

    return render(request, 'pay.html', context)
