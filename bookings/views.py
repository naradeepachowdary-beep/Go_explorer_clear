from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class BookingListView(generics.ListAPIView):
    """List all user bookings"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        from .models import Booking
        return Booking.objects.filter(user=self.request.user)


class BookingDetailView(generics.RetrieveAPIView):
    """Get booking details"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'booking_id'
    
    def get_queryset(self):
        from .models import Booking
        return Booking.objects.filter(user=self.request.user)
