"""
WhatsApp booking system for GoExplorer
Handles booking inquiries and confirmations via WhatsApp
"""
import logging
import json
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from bookings.models import Booking
from notifications.models import NotificationPreference

logger = logging.getLogger(__name__)


class WhatsAppBookingHandler:
    """Handle bookings via WhatsApp"""
    
    # Command patterns
    COMMANDS = {
        'search': 'Search for hotels/buses/packages',
        'book': 'Make a booking',
        'status': 'Check booking status',
        'cancel': 'Cancel booking',
        'help': 'Show available commands',
        'preferences': 'Update notification preferences',
    }
    
    @staticmethod
    def process_message(phone_number, message_text, user=None):
        """
        Process incoming WhatsApp message
        
        Args:
            phone_number: Sender's WhatsApp number
            message_text: Message content
            user: Django user (optional, can be extracted from phone)
        
        Returns:
            dict: Response message
        """
        message_lower = message_text.lower().strip()
        
        # Route to appropriate handler
        if message_lower.startswith('/search'):
            return WhatsAppBookingHandler.handle_search(phone_number, message_text, user)
        elif message_lower.startswith('/book'):
            return WhatsAppBookingHandler.handle_book(phone_number, message_text, user)
        elif message_lower.startswith('/status'):
            return WhatsAppBookingHandler.handle_status(phone_number, message_text, user)
        elif message_lower.startswith('/cancel'):
            return WhatsAppBookingHandler.handle_cancel(phone_number, message_text, user)
        elif message_lower.startswith('/help'):
            return WhatsAppBookingHandler.handle_help()
        elif message_lower.startswith('/preferences'):
            return WhatsAppBookingHandler.handle_preferences(phone_number, message_text, user)
        else:
            return WhatsAppBookingHandler.handle_unknown()
    
    @staticmethod
    def handle_search(phone_number, message_text, user=None):
        """Handle search queries via WhatsApp"""
        # Example: /search hotels bangalore 2026-01-15
        parts = message_text.split()
        
        if len(parts) < 2:
            return {
                'success': False,
                'message': """
                📍 Usage: /search <type> <location> [date]
                
                Examples:
                - /search hotels bangalore
                - /search buses bangalore hyderabad 2026-01-15
                - /search packages goa
                """
            }
        
        search_type = parts[1].lower()
        location = parts[2] if len(parts) > 2 else ''
        date_str = parts[3] if len(parts) > 3 else ''
        
        response = f"""
        🔍 Searching for {search_type} in {location}...
        
        Available options:
        """
        
        if search_type == 'hotels':
            response += """
            🏨 Hotels in {location}:
            1. The Taj Hotel - ⭐⭐⭐⭐⭐ (₹5000/night)
            2. Grand Plaza - ⭐⭐⭐⭐ (₹3500/night)
            3. Budget Inn - ⭐⭐⭐ (₹1500/night)
            
            Reply with hotel number to book (e.g., /book hotel 1)
            """
        elif search_type == 'buses':
            response += """
            🚌 Buses available:
            1. Shatabdi Express - 8:00 AM (₹785)
            2. Royal Coach - 10:00 AM (₹950)
            3. AC Sleeper - 8:00 PM (₹1200)
            
            Reply with bus number to book (e.g., /book bus 1)
            """
        elif search_type == 'packages':
            response += """
            🌴 Tour Packages:
            1. Goa Beach Paradise - 5 days (₹15000)
            2. Himachal Adventure - 7 days (₹18000)
            3. Kerala Backwaters - 4 days (₹12000)
            
            Reply with package number to book (e.g., /book package 1)
            """
        
        return {
            'success': True,
            'message': response.format(location=location)
        }
    
    @staticmethod
    def handle_book(phone_number, message_text, user=None):
        """Handle booking requests via WhatsApp"""
        # Example: /book hotel 1 2026-01-15 2 rooms
        parts = message_text.split()
        
        if len(parts) < 3:
            return {
                'success': False,
                'message': """
                📝 Usage: /book <type> <option> [dates] [quantity]
                
                Examples:
                - /book hotel 1 2026-01-15 1
                - /book bus 2
                - /book package 3 3 (3 travelers)
                """
            }
        
        booking_type = parts[1].lower()
        option_num = parts[2]
        
        # In production, validate and create booking in database
        booking_id = f"WA-{datetime.now().strftime('%Y%m%d%H%M%S')}-{option_num}"
        
        response = f"""
        ✅ Booking Created!
        
        Booking ID: {booking_id}
        Type: {booking_type.capitalize()}
        Option: #{option_num}
        
        💰 Proceed to payment:
        Send /pay {booking_id} to complete payment
        
        For help: /help
        """
        
        return {
            'success': True,
            'message': response,
            'booking_id': booking_id,
            'booking_type': booking_type
        }
    
    @staticmethod
    def handle_status(phone_number, message_text, user=None):
        """Check booking status via WhatsApp"""
        # Example: /status WA-20260102120000-1
        parts = message_text.split()
        
        if len(parts) < 2:
            return {
                'success': False,
                'message': """
                📊 Usage: /status <booking_id>
                
                Example:
                /status WA-20260102120000-1
                """
            }
        
        booking_id = parts[1]
        
        # In production, fetch from database
        response = f"""
        📊 Booking Status
        
        Booking ID: {booking_id}
        Status: ✅ Confirmed
        Property: The Taj Hotel
        Check-in: 2026-01-15
        Check-out: 2026-01-17
        Total Price: ₹10,000
        
        Need help? /help
        """
        
        return {
            'success': True,
            'message': response
        }
    
    @staticmethod
    def handle_cancel(phone_number, message_text, user=None):
        """Handle cancellation requests via WhatsApp"""
        parts = message_text.split()
        
        if len(parts) < 2:
            return {
                'success': False,
                'message': """
                ❌ Usage: /cancel <booking_id>
                
                Example:
                /cancel WA-20260102120000-1
                """
            }
        
        booking_id = parts[1]
        
        response = f"""
        ⏳ Cancellation Processing...
        
        Booking ID: {booking_id}
        Cancellation requested
        
        Refund will be processed within 5-7 business days.
        Your refund amount: ₹9,000 (90% of ₹10,000)
        
        Confirmation sent to email.
        
        Thank you for using GoExplorer!
        """
        
        return {
            'success': True,
            'message': response
        }
    
    @staticmethod
    def handle_preferences(phone_number, message_text, user=None):
        """Update notification preferences via WhatsApp"""
        response = """
        🔔 Notification Preferences
        
        Current settings:
        ✅ Booking confirmations
        ❌ Promotional offers
        ✅ Payment updates
        
        To update, visit:
        https://goexplorer.com/notifications/preferences
        
        Or reply with your preferences!
        """
        
        return {
            'success': True,
            'message': response
        }
    
    @staticmethod
    def handle_help():
        """Show help message"""
        response = """
        🆘 GoExplorer WhatsApp Booking Bot
        
        Available Commands:
        
        🔍 /search <type> <location>
           Search for hotels, buses, packages
        
        📝 /book <type> <option>
           Make a booking
        
        📊 /status <booking_id>
           Check booking status
        
        ❌ /cancel <booking_id>
           Cancel booking
        
        💳 /pay <booking_id>
           Pay for booking
        
        🔔 /preferences
           Update notification settings
        
        Need human support?
        📞 Call: +91-1234-567-890
        💬 Chat: support@goexplorer.com
        """
        
        return {
            'success': True,
            'message': response
        }
    
    @staticmethod
    def handle_unknown():
        """Handle unknown commands"""
        response = """
        ❓ Sorry, I didn't understand that.
        
        Try these commands:
        /help - Show available commands
        /search - Search for bookings
        /book - Make a booking
        /status - Check booking status
        """
        
        return {
            'success': False,
            'message': response
        }


class WhatsAppWebhookHandler:
    """Handle incoming WhatsApp webhooks"""
    
    @staticmethod
    def handle_webhook(data):
        """
        Process incoming webhook from WhatsApp API
        
        Integrate with:
        - Twilio WhatsApp API
        - Meta WhatsApp Business API
        - Nexmo/Vonage
        """
        try:
            phone_number = data.get('from', '')
            message_text = data.get('text', {}).get('body', '')
            message_id = data.get('id', '')
            
            # Try to find user by phone number
            user = None
            try:
                pref = NotificationPreference.objects.get(whatsapp_number=phone_number)
                user = pref.user
            except NotificationPreference.DoesNotExist:
                pass
            
            # Process message
            result = WhatsAppBookingHandler.process_message(phone_number, message_text, user)
            
            # Log interaction
            logger.info(f"WhatsApp message from {phone_number}: {message_text}")
            
            return {
                'success': True,
                'message_id': message_id,
                'response': result.get('message', '')
            }
            
        except Exception as e:
            logger.error(f"WhatsApp webhook error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


# Test messages for development
TEST_WHATSAPP_MESSAGES = {
    'search_hotels': '/search hotels bangalore',
    'search_buses': '/search buses bangalore hyderabad 2026-01-15',
    'search_packages': '/search packages goa',
    'book_hotel': '/book hotel 1 2026-01-15 2',
    'book_bus': '/book bus 2',
    'check_status': '/status WA-20260102120000-1',
    'cancel_booking': '/cancel WA-20260102120000-1',
    'help': '/help',
    'unknown': 'What is the weather like?',
}
