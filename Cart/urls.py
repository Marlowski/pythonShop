from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.show_cart, name="cart-show"),
    path('pay/', views.pay, name="cart-pay"),
]
