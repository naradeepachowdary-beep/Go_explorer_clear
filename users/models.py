from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel


class User(AbstractUser):
    """Custom user model"""
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='users/', null=True, blank=True)
    
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email or self.username


class UserProfile(TimeStampedModel):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal details
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    pincode = models.CharField(max_length=10, blank=True)
    
    # Preferences
    preferred_currency = models.CharField(max_length=3, default='INR')
    newsletter_subscribed = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
