from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Referral

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    referral_code_used = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referral_code_used']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """Check if email is already registered"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_username(self, value):
        """Check if username is already taken"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def create(self, validated_data):
        referral_code_used = validated_data.pop('referral_code_used', None)
        referred_by  = None

        if referral_code_used:
            try:
                referred_by = User.objects.get(referral_code=referral_code_used)
            except User.DoesNotExist:
                raise serializers.ValidationError({"referral_code_used": "Invalid referral code"})

        user = User.objects.create_user(**validated_data, referred_by=referred_by)

        if referred_by:
            Referral.objects.create(referrer=referred_by, referred_user=user, status="successful")

        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])  # Get user by email
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exists! Try register")

        # Authenticate using username
        user = authenticate(username=user.username, password=data['password'])  
        if not user:
            login(self, user)
            raise serializers.ValidationError("Authentication failed! Try again later.")

        tokens = RefreshToken.for_user(user)
        return {
            "access_token": str(tokens.access_token),
            "refresh_token": str(tokens)
        }
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from request
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ReferralSerializer(serializers.ModelSerializer):
    referral_link = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['referral_code', 'referral_link']

    def get_referral_link(self, obj):
        return f"https://127.0.0.1:8000/register?referral={obj.referral_code}"
