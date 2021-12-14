from django.urls import path
from . import views

urlpatterns = [
    path('list/<str:query>', views.rings_list, name='ring-list'),
    path('list/results/<str:query>', views.rings_list, name='ring-list-search'),
    path('product/<int:pk>/', views.ring_detail, name='ring_detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='ring-vote'),
    # path('add/', views.ring_create, name='ring-create'),
    # path('delete/<int:pk>/', views.ring_delete, name='ring-delete'),
]
