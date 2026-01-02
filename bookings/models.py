from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from hotels.models import RoomType
from buses.models import BusSchedule, SeatLayout
from packages.models import PackageDeparture
import uuid


class Booking(TimeStampedModel):
    """Base booking model"""
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
    ]
    
    BOOKING_TYPES = [
        ('hotel', 'Hotel'),
        ('bus', 'Bus'),
        ('package', 'Package'),
    ]
    
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Contact details
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    
    special_requests = models.TextField(blank=True)
    
    # Cancellation
    cancellation_reason = models.TextField(blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booking_id} - {self.user.username} - {self.booking_type}"


class HotelBooking(TimeStampedModel):
    """Hotel booking details"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='hotel_details')
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT)
    
    check_in = models.DateField()
    check_out = models.DateField()
    
    number_of_rooms = models.IntegerField(default=1)
    number_of_adults = models.IntegerField(default=1)
    number_of_children = models.IntegerField(default=0)
    
    total_nights = models.IntegerField()
    
    def __str__(self):
        return f"Hotel Booking - {self.booking.booking_id}"


class BusBooking(TimeStampedModel):
    """Bus booking details"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='bus_details')
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.PROTECT)
    
    journey_date = models.DateField()
    
    def __str__(self):
        return f"Bus Booking - {self.booking.booking_id}"


class BusBookingSeat(models.Model):
    """Seats booked for bus"""
    bus_booking = models.ForeignKey(BusBooking, on_delete=models.CASCADE, related_name='seats')
    seat = models.ForeignKey(SeatLayout, on_delete=models.PROTECT)
    
    passenger_name = models.CharField(max_length=200)
    passenger_age = models.IntegerField()
    passenger_gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    
    class Meta:
        unique_together = ['bus_booking', 'seat']
    
    def __str__(self):
        return f"{self.bus_booking.booking.booking_id} - Seat {self.seat.seat_number}"


class PackageBooking(TimeStampedModel):
    """Package booking details"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='package_details')
    package_departure = models.ForeignKey(PackageDeparture, on_delete=models.PROTECT)
    
    number_of_travelers = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Package Booking - {self.booking.booking_id}"


class PackageBookingTraveler(models.Model):
    """Travelers for package booking"""
    package_booking = models.ForeignKey(PackageBooking, on_delete=models.CASCADE, related_name='travelers')
    
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    passport_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.package_booking.booking.booking_id} - {self.name}"


class Review(TimeStampedModel):
    """Review for bookings"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Review for {self.booking.booking_id} - {self.rating} stars"
