from django.urls import path
from .views import RegisterView, LoginView, SessionLogoutView, ReferralView, ReferralStatsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", SessionLogoutView.as_view(), name="session_logout"),
    path('referrals/', ReferralView.as_view(), name='referrals'),
    path('referral-stats/', ReferralStatsView.as_view(), name='referral-stats'),
]
