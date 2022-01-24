from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profiles/<int:pk>/', views.profile_page, name='user_profile'),
    path('profiles/<int:pk>/edit/', views.profile_edit, name='user_profile_edit'),
]
