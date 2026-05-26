from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, MFASetupView, MFADisableView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('mfa/setup/', MFASetupView.as_view(), name='mfa-setup'),
    path('mfa/disable/', MFADisableView.as_view(), name='mfa-disable'),
]