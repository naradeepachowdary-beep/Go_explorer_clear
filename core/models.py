from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base model with created and updated timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class City(models.Model):
    """Cities for hotels, buses, and packages"""
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    code = models.CharField(max_length=10, unique=True)  # e.g., DEL, BLR, MUM
    is_popular = models.BooleanField(default=False)
    image = models.ImageField(upload_to='cities/', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}, {self.state}"
