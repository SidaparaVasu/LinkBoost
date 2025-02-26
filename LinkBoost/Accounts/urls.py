from django.urls import path
from .views import RegisterView, LoginView, ReferralView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('referrals/', ReferralView.as_view(), name='referrals'),
]
