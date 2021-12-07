from django.urls import path
from . import views

urlpatterns = [
    # path('list/', views.ring_list, name='ring-list'),
    path('product/<int:pk>/', views.ring_detail, name='ring_detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='ring-vote'),
    # path('add/', views.ring_create, name='ring-create'),
    # path('delete/<int:pk>/', views.ring_delete, name='ring-delete'),
]
