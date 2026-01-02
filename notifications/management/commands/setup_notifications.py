from django.core.management.base import BaseCommand
from notifications.models import NotificationTemplate


class Command(BaseCommand):
    help = 'Create default notification templates'

    def handle(self, *args, **options):
        templates_data = [
            {
                'name': 'booking_confirmation',
                'notification_type': 'email',
                'subject': 'Your Booking Confirmation - {booking_id}',
                'body': '''
Dear {user_name},

Your booking has been confirmed!

Booking Details:
- Booking ID: {booking_id}
- Property: {property_name}
- Check-in: {check_in_date}
- Check-out: {check_out_date}
- Total Price: ₹{price}
- Status: CONFIRMED

Please save this confirmation for your records.
You can view/manage your booking at: https://goexplorer.com/bookings/{booking_id}

Thank you for choosing GoExplorer!

Best regards,
GoExplorer Team
                '''
            },
            {
                'name': 'payment_success',
                'notification_type': 'email',
                'subject': 'Payment Confirmed - {booking_id}',
                'body': '''
Dear {user_name},

Your payment has been received successfully!

Payment Details:
- Payment ID: {payment_id}
- Booking ID: {booking_id}
- Amount: ₹{price}
- Date: {payment_date}
- Status: SUCCESS

Your booking is now confirmed. 

Thank you!

GoExplorer Team
                '''
            },
            {
                'name': 'booking_cancelled',
                'notification_type': 'email',
                'subject': 'Booking Cancelled - {booking_id}',
                'body': '''
Dear {user_name},

Your booking has been cancelled as requested.

Booking Details:
- Booking ID: {booking_id}
- Property: {property_name}
- Refund Amount: ₹{refund_amount}
- Refund Status: Processing

The refund will be processed within 5-7 business days.

If you have any questions, please contact our support team.

GoExplorer Team
                '''
            },
            {
                'name': 'reminder',
                'notification_type': 'email',
                'subject': 'Reminder: Your Booking is Coming Up - {booking_id}',
                'body': '''
Dear {user_name},

This is a reminder for your upcoming booking!

Booking Details:
- Booking ID: {booking_id}
- Property: {property_name}
- Check-in: {check_in_date}
- Check-in Time: {check_in_time}

Please arrive on time. If you need to contact the property:
- Phone: {property_phone}
- Email: {property_email}

Have a great stay!

GoExplorer Team
                '''
            },
        ]
        
        created_count = 0
        for template_data in templates_data:
            template, created = NotificationTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    'notification_type': template_data['notification_type'],
                    'subject': template_data['subject'],
                    'body': template_data['body'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Template already exists: {template.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Notification setup complete! Created {created_count} templates.')
        )
