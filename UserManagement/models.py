from django.contrib.auth.models import AbstractUser
from django.db import models
from Cart.models import Cart, CartItem


class MyUser(AbstractUser):
    pass

    profile_picture = models.ImageField(upload_to='picture_uploads/', blank=True, null=True, default="")

    def __str__(self):
        return self.username + " - (" + self.email + ")"

    def get_user_cart_amount(self):
        cart = Cart.objects.filter(user_elem=self.id).first()
        if cart:
            amount = 0
            cart_list = CartItem.objects.filter(cart=cart)
            for item in cart_list:
                amount += item.quantity
            return amount
        else:
            return 0

    # overridden save method
    def save(self, *args, **kwargs):
        if self.profile_picture == "":
            self.profile_picture = 'picture_uploads/default_pic/default-profile.png'
        super().save(*args, **kwargs)

    def is_superuser_or_staff(self):
        return self.is_superuser or self.is_staff
