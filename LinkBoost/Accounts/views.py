from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework import serializers
from .serializers import RegisterSerializer, LoginSerializer, ReferralSerializer

from .models import *

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
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