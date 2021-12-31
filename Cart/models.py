from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.conf import settings
from static.script.utility import get_client_ip


# Create your models here.
def add_item(request, item):
    # get ip-adress of user
    user_ip = get_client_ip(request)

    # get existing shopping cart or create new one if non-existing
    # check if user is logged and query carts accordingly
    if request.user.id is None:
        carts = Cart.objects.filter(user_ip=user_ip)
    else:
        carts = Cart.objects.filter(user_elem=request.user)

    if carts:
        cart = carts.first()
    else:
        if request.user.id is None:
            cart = Cart.objects.create(user_ip=user_ip)
        else:
            cart = Cart.objects.create(user_elem=request.user, user_ip=user_ip)

    # Add elem to cart
    CartItem.objects.create(
        product_id=item.id,
        product_name=item.__str__(),
        price=item.preis,
        quantity=1,
        cart=cart,
    )


class Cart(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    # allow null value on user_elem field for users, that are not logged in
    user_elem = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    user_ip = models.CharField(max_length=1000)

    def get_number_of_items(self):
        cart_items = CartItem.objects.filter(cart=self)
        return len(cart_items)

    def get_total(self):
        total = Decimal(0.0)
        cart_items = CartItem.objects.filter(cart=self)

        for elem in cart_items:
            total += elem.price * elem.quantity
        return total


class CartItem(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class Payment(models.Model):
    credit_card_number = models.CharField(max_length=19)  # 1234 5678 1234 5678
    expiry_date = models.CharField(max_length=7)  # 12/2022
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(default=timezone.now)
    user_type = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
