from django.core.management.base import BaseCommand
from core.models import City


class Command(BaseCommand):
    help = 'Populate sample cities'

    def handle(self, *args, **options):
        cities_data = [
            {'name': 'Delhi', 'state': 'Delhi', 'code': 'DEL', 'is_popular': True},
            {'name': 'Mumbai', 'state': 'Maharashtra', 'code': 'BOM', 'is_popular': True},
            {'name': 'Bangalore', 'state': 'Karnataka', 'code': 'BLR', 'is_popular': True},
            {'name': 'Hyderabad', 'state': 'Telangana', 'code': 'HYD', 'is_popular': True},
            {'name': 'Chennai', 'state': 'Tamil Nadu', 'code': 'MAA', 'is_popular': True},
            {'name': 'Kolkata', 'state': 'West Bengal', 'code': 'CCU', 'is_popular': True},
            {'name': 'Pune', 'state': 'Maharashtra', 'code': 'PNQ', 'is_popular': True},
            {'name': 'Ahmedabad', 'state': 'Gujarat', 'code': 'AMD', 'is_popular': True},
            {'name': 'Jaipur', 'state': 'Rajasthan', 'code': 'JAI', 'is_popular': True},
            {'name': 'Goa', 'state': 'Goa', 'code': 'GOI', 'is_popular': True},
            {'name': 'Chandigarh', 'state': 'Chandigarh', 'code': 'IXC', 'is_popular': False},
            {'name': 'Lucknow', 'state': 'Uttar Pradesh', 'code': 'LKO', 'is_popular': False},
            {'name': 'Kochi', 'state': 'Kerala', 'code': 'COK', 'is_popular': False},
            {'name': 'Indore', 'state': 'Madhya Pradesh', 'code': 'IDR', 'is_popular': False},
            {'name': 'Udaipur', 'state': 'Rajasthan', 'code': 'UDR', 'is_popular': False},
        ]

        for city_data in cities_data:
            city, created = City.objects.get_or_create(
                code=city_data['code'],
                defaults=city_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created city: {city.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'City already exists: {city.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated cities!'))
