from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_booking_confirmation_email(booking_id):
    """Send booking confirmation email"""
    from bookings.models import Booking
    
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        
        subject = f'Booking Confirmation - {booking.booking_id}'
        message = f"""
        Dear {booking.customer_name},
        
        Your booking has been confirmed!
        
        Booking ID: {booking.booking_id}
        Type: {booking.get_booking_type_display()}
        Amount: ₹{booking.total_amount}
        
        Thank you for choosing GoExplorer!
        
        Best regards,
        GoExplorer Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.customer_email],
            fail_silently=False,
        )
        
        return f"Email sent to {booking.customer_email}"
    except Exception as e:
        return f"Error: {str(e)}"


@shared_task
def send_payment_confirmation_email(payment_id):
    """Send payment confirmation email"""
    from payments.models import Payment
    
    try:
        payment = Payment.objects.get(id=payment_id)
        booking = payment.booking
        
        subject = f'Payment Confirmation - {booking.booking_id}'
        message = f"""
        Dear {booking.customer_name},
        
        Your payment has been received successfully!
        
        Booking ID: {booking.booking_id}
        Payment Amount: ₹{payment.amount}
        Transaction ID: {payment.transaction_id}
        
        Thank you for your payment!
        
        Best regards,
        GoExplorer Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.customer_email],
            fail_silently=False,
        )
        
        return f"Payment email sent to {booking.customer_email}"
    except Exception as e:
        return f"Error: {str(e)}"


@shared_task
def generate_invoice_pdf(invoice_id):
    """Generate invoice PDF"""
    from payments.models import Invoice
    # Implement PDF generation logic here
    return f"Invoice PDF generated for {invoice_id}"
