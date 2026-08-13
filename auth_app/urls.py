from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='registration'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/<int:id>/', ProfileView.as_view(), name='profile')
]
