from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Notification, NotificationPreference
from .services import NotificationManager


class NotificationPreferenceUpdateView(LoginRequiredMixin, View):
    """Update notification preferences"""
    
    def get(self, request):
        try:
            preference = request.user.notification_preference
        except NotificationPreference.DoesNotExist:
            preference = NotificationPreference.objects.create(user=request.user)
        
        return render(request, 'notifications/preferences.html', {
            'preference': preference
        })
    
    def post(self, request):
        try:
            preference = request.user.notification_preference
        except NotificationPreference.DoesNotExist:
            preference = NotificationPreference.objects.create(user=request.user)
        
        # Update email preferences
        preference.email_booking_confirmation = request.POST.get('email_booking_confirmation') == 'on'
        preference.email_booking_reminder = request.POST.get('email_booking_reminder') == 'on'
        preference.email_payment_updates = request.POST.get('email_payment_updates') == 'on'
        preference.email_promotions = request.POST.get('email_promotions') == 'on'
        
        # Update WhatsApp preferences
        preference.whatsapp_booking_confirmation = request.POST.get('whatsapp_booking_confirmation') == 'on'
        preference.whatsapp_booking_reminder = request.POST.get('whatsapp_booking_reminder') == 'on'
        preference.whatsapp_payment_updates = request.POST.get('whatsapp_payment_updates') == 'on'
        preference.whatsapp_promotions = request.POST.get('whatsapp_promotions') == 'on'
        preference.whatsapp_number = request.POST.get('whatsapp_number', '')
        
        # Update SMS preferences
        preference.sms_booking_confirmation = request.POST.get('sms_booking_confirmation') == 'on'
        preference.sms_booking_reminder = request.POST.get('sms_booking_reminder') == 'on'
        preference.sms_payment_updates = request.POST.get('sms_payment_updates') == 'on'
        preference.sms_promotions = request.POST.get('sms_promotions') == 'on'
        preference.phone_number = request.POST.get('phone_number', '')
        
        preference.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification preferences updated successfully!'
        })


class NotificationHistoryView(LoginRequiredMixin, ListView):
    """View notification history"""
    model = Notification
    template_name = 'notifications/history.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class NotificationDetailView(LoginRequiredMixin, DetailView):
    """View notification details"""
    model = Notification
    template_name = 'notifications/detail.html'
    context_object_name = 'notification'
    pk_url_kwarg = 'notification_id'
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


@login_required
@require_http_methods(["POST"])
def send_test_notification(request):
    """Send test notification to user"""
    notification_type = request.POST.get('type', 'email')
    
    test_data = {
        'booking_id': 'TEST-001',
        'property_name': 'Test Hotel',
        'booking_date': '2026-01-15',
        'booking_type': 'Hotel',
        'price': '5000'
    }
    
    result = None
    if notification_type == 'email':
        from .services import EmailService
        result = EmailService.send_booking_confirmation(request.user, test_data)
    elif notification_type == 'whatsapp':
        from .services import WhatsAppService
        try:
            pref = request.user.notification_preference
            if pref.whatsapp_number:
                result = WhatsAppService.send_booking_confirmation(request.user, test_data)
        except:
            pass
    elif notification_type == 'sms':
        from .services import SMSService
        try:
            pref = request.user.notification_preference
            if pref.phone_number:
                result = SMSService.send_booking_confirmation(request.user, test_data)
        except:
            pass
    
    return JsonResponse({
        'success': result is not None,
        'message': f'Test {notification_type} notification sent!'
    })
