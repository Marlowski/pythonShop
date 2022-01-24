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
        # make sure to not query carts that might have the same ip, but already have a user-elem set
        carts = Cart.objects.filter(user_ip=user_ip, user_elem=None)
    else:
        carts = Cart.objects.filter(user_elem=request.user)

    if carts:
        cart = carts.first()
    else:
        if request.user.id is None:
            cart = Cart.objects.create(user_ip=user_ip)
        else:
            cart = Cart.objects.create(user_elem=request.user, user_ip=user_ip)

    # check if elem already exist -> raise quantity
    same_product_existing = CartItem.objects.filter(cart=cart, product_id=item.id).first()
    if same_product_existing is not None:
        same_product_existing.quantity += 1
        same_product_existing.save()
    else:
        # Add elem to cart
        CartItem.objects.create(
            product_id=item.id,
            product_name=item.__str__(),
            product_img_url=item.product_img_url,
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
    product_img_url = models.ImageField(upload_to='product_images/', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class Payment(models.Model):
    user_elem = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=200, null=True)
    credit_card_number = models.CharField(max_length=19)  # 1234 5678 1234 5678
    expiry_date = models.CharField(max_length=7)  # 12/2022
    items_id = models.CharField(max_length=3000)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(default=timezone.now)
