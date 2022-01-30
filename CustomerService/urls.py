from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start'),
    path('create/', views.product_create, name='product-create'),
    path('list/', views.product_list, name='list'),
    path('delete/<int:pk>/', views.product_delete, name='product-delete'),
]
