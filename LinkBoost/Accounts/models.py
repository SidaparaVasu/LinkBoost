from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals'
    )

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4().hex[:20])  # Generate unique referral code
        super().save(*args, **kwargs)


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrer_referrals")
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referred_by_referral")
    date_referred = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("successful", "Successful")], default="pending")

    def __str__(self):
        return f"{self.referrer.username} → {self.referred_user.username} ({self.status})"
