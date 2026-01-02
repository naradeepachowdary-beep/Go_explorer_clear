from django.db import models
from django.core.validators import MinValueValidator
from core.models import TimeStampedModel, City


class Package(TimeStampedModel):
    """Holiday package model"""
    PACKAGE_TYPES = [
        ('adventure', 'Adventure'),
        ('beach', 'Beach'),
        ('cultural', 'Cultural'),
        ('family', 'Family'),
        ('honeymoon', 'Honeymoon'),
        ('pilgrimage', 'Pilgrimage'),
        ('wildlife', 'Wildlife'),
        ('luxury', 'Luxury'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    
    destination_cities = models.ManyToManyField(City, related_name='packages')
    
    duration_days = models.IntegerField(validators=[MinValueValidator(1)])
    duration_nights = models.IntegerField(validators=[MinValueValidator(0)])
    
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    image = models.ImageField(upload_to='packages/', null=True, blank=True)
    
    # Inclusions
    includes_hotel = models.BooleanField(default=True)
    includes_transport = models.BooleanField(default=True)
    includes_meals = models.BooleanField(default=True)
    includes_sightseeing = models.BooleanField(default=True)
    includes_guide = models.BooleanField(default=False)
    
    # Meal plan
    breakfast_included = models.BooleanField(default=True)
    lunch_included = models.BooleanField(default=False)
    dinner_included = models.BooleanField(default=False)
    
    max_group_size = models.IntegerField(default=10)
    min_group_size = models.IntegerField(default=2)
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-is_featured', '-rating', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.duration_days}D/{self.duration_nights}N"


class PackageImage(models.Model):
    """Additional images for packages"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='packages/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.package.name} - Image"


class PackageItinerary(models.Model):
    """Day-by-day itinerary for packages"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='itinerary')
    day_number = models.IntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200)
    description = models.TextField()
    activities = models.TextField(help_text='Comma-separated list of activities')
    
    meals_included = models.CharField(max_length=100, blank=True, help_text='e.g., Breakfast, Lunch')
    accommodation = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['package', 'day_number']
        unique_together = ['package', 'day_number']
    
    def __str__(self):
        return f"{self.package.name} - Day {self.day_number}"


class PackageInclusion(models.Model):
    """What's included in the package"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='inclusions')
    description = models.CharField(max_length=200)
    is_included = models.BooleanField(default=True)  # True for inclusion, False for exclusion
    
    class Meta:
        ordering = ['-is_included', 'description']
    
    def __str__(self):
        return f"{self.package.name} - {self.description}"


class PackageDeparture(TimeStampedModel):
    """Package departure dates and pricing"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='departures')
    departure_date = models.DateField()
    return_date = models.DateField()
    
    available_slots = models.IntegerField(validators=[MinValueValidator(0)])
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['departure_date']
        unique_together = ['package', 'departure_date']
    
    def __str__(self):
        return f"{self.package.name} - {self.departure_date}"
