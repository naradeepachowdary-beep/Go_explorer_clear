from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import TimeStampedModel, City


class Hotel(TimeStampedModel):
    """Hotel model"""
    STAR_RATINGS = [
        (1, '1 Star'),
        (2, '2 Star'),
        (3, '3 Star'),
        (4, '4 Star'),
        (5, '5 Star'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    star_rating = models.IntegerField(choices=STAR_RATINGS, default=3)
    review_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    review_count = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Amenities
    has_wifi = models.BooleanField(default=True)
    has_parking = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=True)
    
    checkin_time = models.TimeField(default='14:00')
    checkout_time = models.TimeField(default='11:00')
    
    # GST (Goods and Services Tax)
    gst_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=18.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="GST percentage (default: 18%)"
    )
    
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    
    class Meta:
        ordering = ['-is_featured', '-review_rating', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.city.name}"


class HotelImage(models.Model):
    """Additional images for hotels"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotels/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.hotel.name} - Image"


class RoomType(TimeStampedModel):
    """Room types for hotels"""
    ROOM_TYPES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Suite'),
        ('family', 'Family Room'),
        ('executive', 'Executive Room'),
    ]
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='standard')
    description = models.TextField()
    
    max_occupancy = models.IntegerField(default=2)
    number_of_beds = models.IntegerField(default=1)
    room_size = models.IntegerField(help_text='Size in square feet', null=True, blank=True)
    
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Room amenities
    has_balcony = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=True)
    has_minibar = models.BooleanField(default=False)
    has_safe = models.BooleanField(default=False)
    
    total_rooms = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    
    image = models.ImageField(upload_to='hotels/rooms/', null=True, blank=True)
    
    class Meta:
        ordering = ['hotel', 'base_price']
    
    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class RoomAvailability(models.Model):
    """Track room availability by date"""
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    available_rooms = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['room_type', 'date']
        ordering = ['date']
    
    def __str__(self):
        return f"{self.room_type} - {self.date}"
