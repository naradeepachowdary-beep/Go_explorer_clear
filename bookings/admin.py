from django.contrib import admin
from .models import (
    Booking, HotelBooking, BusBooking, BusBookingSeat,
    PackageBooking, PackageBookingTraveler, Review
)


class HotelBookingInline(admin.StackedInline):
    model = HotelBooking
    extra = 0


class BusBookingSeatInline(admin.TabularInline):
    model = BusBookingSeat
    extra = 1


class BusBookingInline(admin.StackedInline):
    model = BusBooking
    extra = 0


class PackageBookingTravelerInline(admin.TabularInline):
    model = PackageBookingTraveler
    extra = 1


class PackageBookingInline(admin.StackedInline):
    model = PackageBooking
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'booking_type', 'status', 'total_amount', 'paid_amount', 'created_at']
    list_filter = ['booking_type', 'status', 'created_at']
    search_fields = ['booking_id', 'user__username', 'user__email', 'customer_email', 'customer_phone']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'user', 'booking_type', 'status')
        }),
        ('Financial', {
            'fields': ('total_amount', 'paid_amount')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'special_requests')
        }),
        ('Cancellation', {
            'fields': ('cancellation_reason', 'cancelled_at', 'refund_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_inline_instances(self, request, obj=None):
        """Show appropriate inline based on booking type"""
        if not obj:
            return []
        
        inlines = []
        if obj.booking_type == 'hotel':
            inlines.append(HotelBookingInline(self.model, self.admin_site))
        elif obj.booking_type == 'bus':
            bus_inline = BusBookingInline(self.model, self.admin_site)
            inlines.append(bus_inline)
        elif obj.booking_type == 'package':
            inlines.append(PackageBookingInline(self.model, self.admin_site))
        
        return inlines


@admin.register(BusBooking)
class BusBookingAdmin(admin.ModelAdmin):
    list_display = ['booking', 'bus_schedule', 'journey_date']
    list_filter = ['journey_date']
    search_fields = ['booking__booking_id', 'booking__user__username']
    inlines = [BusBookingSeatInline]


@admin.register(PackageBooking)
class PackageBookingAdmin(admin.ModelAdmin):
    list_display = ['booking', 'package_departure', 'number_of_travelers']
    list_filter = ['package_departure__departure_date']
    search_fields = ['booking__booking_id', 'booking__user__username']
    inlines = [PackageBookingTravelerInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['booking__booking_id', 'comment']
    list_editable = ['is_approved']
