from rest_framework import serializers
from .models import Bus, BusRoute, BusSchedule, BusOperator, SeatLayout


class BusOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusOperator
        fields = ['id', 'name', 'logo', 'rating']


class BusSerializer(serializers.ModelSerializer):
    operator = BusOperatorSerializer(read_only=True)
    
    class Meta:
        model = Bus
        fields = [
            'id', 'operator', 'bus_number', 'bus_name', 'bus_type',
            'total_seats', 'has_ac', 'has_wifi', 'has_charging_point',
            'has_blanket', 'has_water_bottle', 'has_tv'
        ]


class BusRouteSerializer(serializers.ModelSerializer):
    bus = BusSerializer(read_only=True)
    source_city_name = serializers.CharField(source='source_city.name', read_only=True)
    destination_city_name = serializers.CharField(source='destination_city.name', read_only=True)
    
    class Meta:
        model = BusRoute
        fields = [
            'id', 'bus', 'route_name', 'source_city', 'source_city_name',
            'destination_city', 'destination_city_name', 'departure_time',
            'arrival_time', 'duration_hours', 'distance_km', 'base_fare'
        ]


class BusScheduleSerializer(serializers.ModelSerializer):
    route = BusRouteSerializer(read_only=True)
    
    class Meta:
        model = BusSchedule
        fields = ['id', 'route', 'date', 'available_seats', 'fare', 'is_active']


class SeatLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatLayout
        fields = ['id', 'seat_number', 'seat_type', 'row', 'column', 'deck']
