from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from Accounts.models import *

User = get_user_model()



def user_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))
    return _wrapped_view


def indexPage(request):
    try:
        if request.session['is_authenticated']:
            return redirect('/home')
    except:
        return render(request, 'index.html')

def register(request):
    print("GET Params:", request.GET)
    referral_code = request.GET.get("referral", None)
    print("Referral Code:", referral_code)
    return render(request, 'register.html', {"referral_code": referral_code})

def login(request):
    return render(request, 'login.html')


def home_view(request):
    if request.session['is_authenticated']:
        user = User.objects.filter(username=request.session['username']).first()

        referral_link = f"http://127.0.0.1:8000/register?referral={user.referral_code}"

        # Fetch referred users along with their referral status
        referred_users = Referral.objects.filter(referrer=user).select_related("referred_user")

        # Fetch referral statistics
        total_referrals = referred_users.count()
        successful_referrals = referred_users.filter(status="successful").count()

        return render(request, "home.html", {
            "referral_link": referral_link,
            "referred_users": referred_users,
            "total_referrals": total_referrals,
            "successful_referrals": successful_referrals,
        })
    
    return redirect('login')