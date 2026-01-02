from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from core.models import City
from hotels.models import Hotel, RoomType, HotelImage, RoomAvailability


class Command(BaseCommand):
    help = 'Populate database with sample hotels'

    def handle(self, *args, **kwargs):
        # Get cities
        delhi = City.objects.get(name='Delhi')
        mumbai = City.objects.get(name='Mumbai')
        bangalore = City.objects.get(name='Bangalore')
        goa = City.objects.get(name='Goa')

        # Create Hotels
        hotels_data = [
            {
                'name': 'The Grand Palace Hotel',
                'city': delhi,
                'address': '12 Connaught Place, New Delhi',
                'description': 'Luxury 5-star hotel in the heart of Delhi with world-class amenities',
                'star_rating': 5,
                'contact_phone': '+91-11-2334-5678',
                'contact_email': 'contact@grandpalace.com',
                'amenities': ['WiFi', 'Pool', 'Gym', 'Spa', 'Restaurant'],
            },
            {
                'name': 'Mumbai Skyline Resort',
                'city': mumbai,
                'address': '45 Marine Drive, Mumbai',
                'description': 'Stunning sea-view hotel with modern facilities and excellent service',
                'star_rating': 4,
                'contact_phone': '+91-22-2555-6789',
                'contact_email': 'info@mumbaisk yline.com',
                'amenities': ['WiFi', 'Pool', 'Gym', 'Restaurant'],
            },
            {
                'name': 'Bangalore Tech Suites',
                'city': bangalore,
                'address': '78 MG Road, Bangalore',
                'description': 'Business-friendly hotel with high-speed internet and conference facilities',
                'star_rating': 4,
                'contact_phone': '+91-80-4123-4567',
                'contact_email': 'reservations@bangaloretech.com',
                'amenities': ['WiFi', 'Gym', 'Restaurant'],
            },
            {
                'name': 'Goa Beach Paradise',
                'city': goa,
                'address': 'Calangute Beach Road, Goa',
                'description': 'Beachfront resort with stunning ocean views and water sports',
                'star_rating': 5,
                'contact_phone': '+91-832-2277-8899',
                'contact_email': 'bookings@goabeachparadise.com',
                'amenities': ['WiFi', 'Pool', 'Spa', 'Restaurant'],
            },
            {
                'name': 'Delhi Airport Inn',
                'city': delhi,
                'address': 'Near IGI Airport, New Delhi',
                'description': 'Convenient budget hotel near the airport with comfortable rooms',
                'star_rating': 3,
                'contact_phone': '+91-11-4456-7890',
                'contact_email': 'stay@delhiairportinn.com',
                'amenities': ['WiFi', 'Restaurant'],
            },
        ]

        for hotel_data in hotels_data:
            amenities = hotel_data.pop('amenities')
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults={
                    **hotel_data,
                    'has_wifi': 'WiFi' in amenities,
                    'has_parking': True,
                    'has_pool': 'Pool' in amenities,
                    'has_gym': 'Gym' in amenities,
                    'has_spa': 'Spa' in amenities,
                    'has_restaurant': 'Restaurant' in amenities,
                    'has_ac': True,
                    'review_rating': 4.5,
                    'review_count': 150,
                    'latitude': 0.0,
                    'longitude': 0.0,
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created hotel: {hotel.name}'))
                
                # Create room types
                room_types = [
                    {
                        'name': 'Standard Room',
                        'room_type': 'standard',
                        'description': 'Comfortable room with basic amenities',
                        'base_price': 2000 if hotel.star_rating >= 4 else 1500,
                        'max_occupancy': 2,
                        'number_of_beds': 1,
                        'room_size': 250,
                        'total_rooms': 10,
                    },
                    {
                        'name': 'Deluxe Room',
                        'room_type': 'deluxe',
                        'description': 'Spacious room with premium amenities',
                        'base_price': 3500 if hotel.star_rating >= 4 else 2500,
                        'max_occupancy': 3,
                        'number_of_beds': 2,
                        'room_size': 350,
                        'total_rooms': 5,
                    },
                    {
                        'name': 'Suite',
                        'room_type': 'suite',
                        'description': 'Luxurious suite with living area',
                        'base_price': 6000 if hotel.star_rating >= 4 else 4000,
                        'max_occupancy': 4,
                        'number_of_beds': 2,
                        'room_size': 500,
                        'total_rooms': 3,
                    },
                ]
                
                for room_data in room_types:
                    total_rooms = room_data.pop('total_rooms')
                    room_type = RoomType.objects.create(
                        hotel=hotel,
                        **room_data,
                        has_tv=True,
                        has_minibar=hotel.star_rating >= 4,
                        has_balcony=room_data['room_type'] in ['deluxe', 'suite'],
                        total_rooms=total_rooms,
                        is_available=True,
                    )
                    
                    # Create room availability for next 90 days
                    today = date.today()
                    for i in range(90):
                        availability_date = today + timedelta(days=i)
                        RoomAvailability.objects.create(
                            room_type=room_type,
                            date=availability_date,
                            available_rooms=total_rooms,
                            price=room_data['base_price'],
                        )
                
                self.stdout.write(self.style.SUCCESS(f'  Created {len(room_types)} room types with availability'))

        self.stdout.write(self.style.SUCCESS('\nSuccessfully populated hotels!'))
        self.stdout.write(self.style.SUCCESS(f'Total hotels created: {len(hotels_data)}'))
