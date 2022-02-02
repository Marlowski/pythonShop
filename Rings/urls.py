from django.urls import path
# important import so in 'ring-list' back btn can use CustomerService urls
import CustomerService.urls
from . import views

urlpatterns = [
    path('list/<str:query>', views.rings_list, name='ring-list'),
    path('list/results/<str:query>', views.rings_list, name='ring-list-search'),
    path('product/<int:pk>/', views.ring_detail, name='ring_detail'),
    path('product/<int:pk>/edit', views.ring_edit, name='ring-edit'),
]
