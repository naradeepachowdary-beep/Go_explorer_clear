from django.contrib import admin
from .models import NotificationTemplate, Notification, NotificationPreference


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'notification_type', 'is_active', 'updated_at']
    list_filter = ['notification_type', 'is_active', 'created_at']
    search_fields = ['name', 'body']
    fieldsets = (
        ('Template Info', {
            'fields': ('name', 'notification_type', 'is_active')
        }),
        ('Content', {
            'fields': ('subject', 'body'),
            'description': 'Use {variable_name} format for placeholders. Available: {user_name}, {booking_id}, {hotel_name}, {bus_name}, {package_name}, {price}, {date}, {status}'
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'status', 'sent_at', 'created_at']
    list_filter = ['notification_type', 'status', 'created_at']
    search_fields = ['recipient', 'booking_id', 'payment_id', 'body']
    readonly_fields = ['created_at', 'updated_at', 'sent_at', 'provider_reference']
    fieldsets = (
        ('Recipient Info', {
            'fields': ('user', 'recipient', 'notification_type')
        }),
        ('Message', {
            'fields': ('subject', 'body')
        }),
        ('Status', {
            'fields': ('status', 'error_message', 'provider_reference', 'sent_at')
        }),
        ('References', {
            'fields': ('booking_id', 'payment_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'whatsapp_number', 'phone_number']
    search_fields = ['user__username', 'whatsapp_number', 'phone_number']
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Preferences', {
            'fields': ('email_booking_confirmation', 'email_booking_reminder', 'email_payment_updates', 'email_promotions'),
            'classes': ('collapse',)
        }),
        ('WhatsApp Preferences', {
            'fields': ('whatsapp_number', 'whatsapp_booking_confirmation', 'whatsapp_booking_reminder', 'whatsapp_payment_updates', 'whatsapp_promotions'),
            'classes': ('collapse',)
        }),
        ('SMS Preferences', {
            'fields': ('phone_number', 'sms_booking_confirmation', 'sms_booking_reminder', 'sms_payment_updates', 'sms_promotions'),
            'classes': ('collapse',)
        }),
    )
