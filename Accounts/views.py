from django.shortcuts import render, redirect, reverse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework import serializers
from .serializers import RegisterSerializer, LoginSerializer, ReferralSerializer

from .models import *

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        referral_code = request.POST.get("referral_code")  # Capture referral code from form
        print("Received Referral Code:", referral_code)  # Debugging

        # Ensure the referral code is passed to serializer
        data = request.data.copy()  # Create a mutable copy of request data
        data['referral_code_used'] = referral_code

        serializer = RegisterSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()  # Save new user

            # Debugging: Check if user is correctly linked
            print("New User:", user.username, "| Referred By:", user.referred_by)

            return render(request, 'login.html')  # Redirect to login page

        # Extract error messages
        error_messages = [error[0] for error in serializer.errors.values()]
        return render(request, 'register.html', {"message": error_messages})



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            
            email = request.POST.get("email")
            user_data = User.objects.filter(email=email).first()

            request.session['username'] = user_data.username
            request.session['email'] = user_data.email
            request.session['referral_code'] = user_data.referral_code
            request.session['is_authenticated'] = True

            return redirect(reverse('home_view'))
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        # Extract only error messages (not error details)
        error_messages = [error[0] for error in serializer.errors.values()]

        return render(request, 'login.html', {"message": error_messages})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

class ReferralView(RetrieveAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class ReferralStatsSerializer(serializers.Serializer):
    total_referrals = serializers.IntegerField()
    successful_referrals = serializers.IntegerField()


class ReferralStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_referrals = Referral.objects.filter(referrer=user).count()
        successful_referrals = Referral.objects.filter(referrer=user, status="successful").count()

        return Response({
            "total_referrals": total_referrals,
            "successful_referrals": successful_referrals    
        })
    

class SessionLogoutView(APIView):
    def get(self, request):
        logout(request)  # Logs out the user
        return redirect("/login")  # Redirect to login page