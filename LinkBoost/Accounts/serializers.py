from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    referral_code_used = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referral_code_used']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        referral_code_used = validated_data.pop('referral_code_used', None)
        referrer = None

        if referral_code_used:
            try:
                referrer = User.objects.get(referral_code=referral_code_used)
            except User.DoesNotExist:
                raise serializers.ValidationError({"referral_code_used": "Invalid referral code"})

        user = User.objects.create_user(**validated_data, referred_by=referrer)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])  # Get user by email
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email!")

        # Authenticate using username
        user = authenticate(username=user.username, password=data['password'])  
        if not user:
            raise serializers.ValidationError("Invalid password")

        tokens = RefreshToken.for_user(user)
        return {
            "access_token": str(tokens.access_token),
            "refresh_token": str(tokens)
        }
    


class ReferralSerializer(serializers.ModelSerializer):
    referral_link = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['referral_code', 'referral_link']

    def get_referral_link(self, obj):
        return f"https://127.0.0.1:8000/register?referral={obj.referral_code}"
