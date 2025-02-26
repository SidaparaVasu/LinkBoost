from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    referral_code_used = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referral_code_used']

    def create(self, validated_data):
        referral_code_used = validated_data.pop('referral_code_used', None)
        referrer = None

        if referral_code_used:
            try:
                referrer = User.objects.get(referral_code=referral_code_used)
            except User.DoesNotExist:
                raise serializers.ValidationError({"referral_code_used": "Invalid referral code"})

        user = User.objects.create_user(**validated_data)
        user.referred_by = referrer
        user.save()
        return user
