from django.contrib import admin
from .models import Payment, Invoice


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_method', 'status', 'transaction_date', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['booking__booking_id', 'transaction_id', 'gateway_payment_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Booking & Amount', {
            'fields': ('booking', 'amount', 'currency')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'status', 'transaction_id', 'transaction_date')
        }),
        ('Gateway Details', {
            'fields': ('gateway_payment_id', 'gateway_order_id', 'gateway_signature', 'gateway_response')
        }),
        ('Refund', {
            'fields': ('refund_id', 'refund_amount', 'refund_date')
        }),
        ('Additional', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'booking', 'billing_name', 'total_amount', 'invoice_date']
    list_filter = ['invoice_date']
    search_fields = ['invoice_number', 'booking__booking_id', 'billing_name', 'billing_email']
    readonly_fields = ['invoice_number', 'invoice_date']
    
    fieldsets = (
        ('Invoice Details', {
            'fields': ('invoice_number', 'invoice_date', 'booking')
        }),
        ('Billing Information', {
            'fields': ('billing_name', 'billing_email', 'billing_phone', 'billing_address')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Tax Details', {
            'fields': ('cgst', 'sgst', 'igst')
        }),
        ('PDF', {
            'fields': ('pdf_file',)
        }),
    )
