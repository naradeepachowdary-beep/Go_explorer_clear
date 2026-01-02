from django.contrib import admin
from .models import Package, PackageImage, PackageItinerary, PackageInclusion, PackageDeparture


class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1


class PackageItineraryInline(admin.TabularInline):
    model = PackageItinerary
    extra = 1
    fields = ['day_number', 'title', 'description', 'meals_included', 'accommodation']


class PackageInclusionInline(admin.TabularInline):
    model = PackageInclusion
    extra = 1


class PackageDepartureInline(admin.TabularInline):
    model = PackageDeparture
    extra = 1
    fields = ['departure_date', 'return_date', 'available_slots', 'price_per_person', 'is_active']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'package_type', 'duration_days', 'duration_nights', 'starting_price', 'is_featured', 'is_active']
    list_filter = ['package_type', 'is_featured', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'is_active']
    filter_horizontal = ['destination_cities']
    inlines = [PackageImageInline, PackageItineraryInline, PackageInclusionInline, PackageDepartureInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'package_type', 'destination_cities')
        }),
        ('Duration', {
            'fields': ('duration_days', 'duration_nights')
        }),
        ('Pricing', {
            'fields': ('starting_price',)
        }),
        ('Inclusions', {
            'fields': ('includes_hotel', 'includes_transport', 'includes_meals', 'includes_sightseeing', 'includes_guide')
        }),
        ('Meal Plan', {
            'fields': ('breakfast_included', 'lunch_included', 'dinner_included')
        }),
        ('Group Size', {
            'fields': ('min_group_size', 'max_group_size')
        }),
        ('Rating & Reviews', {
            'fields': ('rating', 'review_count')
        }),
        ('Media & Status', {
            'fields': ('image', 'is_featured', 'is_active')
        }),
    )


@admin.register(PackageDeparture)
class PackageDepartureAdmin(admin.ModelAdmin):
    list_display = ['package', 'departure_date', 'return_date', 'available_slots', 'price_per_person', 'is_active']
    list_filter = ['is_active', 'departure_date', 'package__package_type']
    search_fields = ['package__name']
    date_hierarchy = 'departure_date'
    list_editable = ['available_slots', 'price_per_person', 'is_active']
