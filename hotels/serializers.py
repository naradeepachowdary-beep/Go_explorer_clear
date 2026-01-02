from rest_framework import serializers
from .models import Hotel, RoomType, HotelImage, RoomAvailability


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'image', 'caption', 'is_primary']


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            'id', 'name', 'room_type', 'description', 'max_occupancy',
            'number_of_beds', 'room_size', 'base_price', 'has_balcony',
            'has_tv', 'has_minibar', 'has_safe', 'total_rooms',
            'is_available', 'image'
        ]


class HotelListSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'city', 'city_name', 'address', 'star_rating',
            'review_rating', 'review_count', 'image', 'is_featured'
        ]


class HotelDetailSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    room_types = RoomTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'description', 'city', 'city_name', 'address',
            'latitude', 'longitude', 'star_rating', 'review_rating',
            'review_count', 'image', 'images', 'has_wifi', 'has_parking',
            'has_pool', 'has_gym', 'has_restaurant', 'has_spa', 'has_ac',
            'checkin_time', 'checkout_time', 'contact_phone', 'contact_email',
            'room_types', 'is_featured'
        ]
