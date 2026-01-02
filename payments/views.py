from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import razorpay
import hmac
import hashlib


class CreatePaymentOrderView(APIView):
    """Create Razorpay order"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        from bookings.models import Booking
        from .models import Payment
        
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')
        
        try:
            booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create order
        order_data = {
            'amount': int(float(amount) * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': str(booking.booking_id),
            'notes': {
                'booking_id': str(booking.booking_id),
                'user_id': str(request.user.id)
            }
        }
        
        order = client.order.create(data=order_data)
        
        # Create payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_method='razorpay',
            gateway_order_id=order['id']
        )
        
        return Response({
            'order_id': order['id'],
            'amount': amount,
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID
        })


class VerifyPaymentView(APIView):
    """Verify Razorpay payment"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        from .models import Payment
        
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')
        
        # Verify signature
        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        try:
            payment = Payment.objects.get(gateway_order_id=razorpay_order_id)
            
            if generated_signature == razorpay_signature:
                payment.status = 'success'
                payment.gateway_payment_id = razorpay_payment_id
                payment.gateway_signature = razorpay_signature
                payment.save()
                
                # Update booking
                booking = payment.booking
                booking.paid_amount += payment.amount
                if booking.paid_amount >= booking.total_amount:
                    booking.status = 'confirmed'
                booking.save()
                
                return Response({'status': 'success', 'message': 'Payment verified successfully'})
            else:
                payment.status = 'failed'
                payment.save()
                return Response({'status': 'failed', 'message': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)


class RazorpayWebhookView(APIView):
    """Handle Razorpay webhooks"""
    permission_classes = []
    
    def post(self, request):
        # Handle webhook events
        event = request.data.get('event')
        
        # Process different event types
        if event == 'payment.captured':
            # Handle payment captured
            pass
        elif event == 'payment.failed':
            # Handle payment failed
            pass
        elif event == 'refund.created':
            # Handle refund
            pass
        
        return Response({'status': 'ok'})
