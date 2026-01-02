"""
Notification models for email, WhatsApp, and SMS
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class NotificationTemplate(models.Model):
    """Template for notifications"""
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
    ]
    
    TEMPLATE_NAMES = [
        ('booking_confirmation', 'Booking Confirmation'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('payment_success', 'Payment Success'),
        ('payment_failed', 'Payment Failed'),
        ('reminder', 'Booking Reminder'),
        ('status_update', 'Status Update'),
    ]
    
    name = models.CharField(max_length=100, choices=TEMPLATE_NAMES, unique=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    subject = models.CharField(max_length=200, help_text="For email notifications")
    body = models.TextField(help_text="Use {variable_name} for placeholders")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Notification Templates"
    
    def __str__(self):
        return f"{self.get_name_display()} ({self.get_notification_type_display()})"


class Notification(models.Model):
    """Track sent notifications"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ]
    
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.CharField(max_length=255, help_text="Email, phone, or WhatsApp ID")
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    provider_reference = models.CharField(max_length=255, blank=True, help_text="Reference from email/SMS provider")
    error_message = models.TextField(blank=True, help_text="Error details if failed")
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Related booking/payment info
    booking_id = models.CharField(max_length=100, blank=True)
    payment_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', 'notification_type']),
        ]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.recipient} ({self.get_status_display()})"
    
    def mark_sent(self, provider_ref=''):
        """Mark notification as sent"""
        self.status = 'sent'
        self.sent_at = timezone.now()
        if provider_ref:
            self.provider_reference = provider_ref
        self.save()
    
    def mark_failed(self, error_msg=''):
        """Mark notification as failed"""
        self.status = 'failed'
        if error_msg:
            self.error_message = error_msg
        self.save()


class NotificationPreference(models.Model):
    """User preferences for notifications"""
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preference')
    
    # Email preferences
    email_booking_confirmation = models.BooleanField(default=True)
    email_booking_reminder = models.BooleanField(default=True)
    email_payment_updates = models.BooleanField(default=True)
    email_promotions = models.BooleanField(default=False)
    
    # WhatsApp preferences
    whatsapp_booking_confirmation = models.BooleanField(default=True)
    whatsapp_booking_reminder = models.BooleanField(default=False)
    whatsapp_payment_updates = models.BooleanField(default=True)
    whatsapp_promotions = models.BooleanField(default=False)
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text="WhatsApp number with country code")
    
    # SMS preferences
    sms_booking_confirmation = models.BooleanField(default=False)
    sms_booking_reminder = models.BooleanField(default=False)
    sms_payment_updates = models.BooleanField(default=False)
    sms_promotions = models.BooleanField(default=False)
    
    # Phone for SMS
    phone_number = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Notification Preferences"
