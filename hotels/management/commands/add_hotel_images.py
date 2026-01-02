"""
Management command to add images to hotels
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from io import BytesIO
from hotels.models import Hotel, HotelImage


class Command(BaseCommand):
    help = 'Add images to hotels from internet'

    HOTEL_IMAGES = {
        'Bangalore Tech Suites': [
            'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1571896349842-b58d8ceb4ee0?w=800&h=600&fit=crop',
        ],
        'Mumbai Luxury': [
            'https://images.unsplash.com/photo-1594822303529-c80c806667a3?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&h=600&fit=crop',
        ],
        'Delhi Heritage': [
            'https://images.unsplash.com/photo-1445991842772-097fea258e7b?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1579156069263-13b3f59eaed2?w=800&h=600&fit=crop',
        ],
        'Goa Beach Resort': [
            'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=800&h=600&fit=crop',
        ],
        'Jaipur Palace Hotel': [
            'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1553531088-f352d4f89b94?w=800&h=600&fit=crop',
        ],
    }

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to add hotel images...'))

        for hotel_name, image_urls in self.HOTEL_IMAGES.items():
            try:
                hotel = Hotel.objects.get(name=hotel_name)
                
                # Add first image as main image if not already set
                if not hotel.image:
                    self.stdout.write(f'Adding main image to {hotel_name}...')
                    try:
                        response = requests.get(image_urls[0], timeout=5)
                        if response.status_code == 200:
                            image_name = f'{hotel_name.lower().replace(" ", "_")}_main.jpg'
                            hotel.image.save(
                                image_name,
                                ContentFile(response.content),
                                save=True
                            )
                            self.stdout.write(self.style.SUCCESS(f'✓ Added main image to {hotel_name}'))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'⚠ Failed to download image for {hotel_name}: {str(e)}'))
                
                # Add additional images to gallery
                for idx, image_url in enumerate(image_urls[1:], start=1):
                    try:
                        if not HotelImage.objects.filter(hotel=hotel, caption__icontains=f'Gallery {idx}').exists():
                            response = requests.get(image_url, timeout=5)
                            if response.status_code == 200:
                                image_name = f'{hotel_name.lower().replace(" ", "_")}_gallery_{idx}.jpg'
                                HotelImage.objects.create(
                                    hotel=hotel,
                                    caption=f'Gallery {idx}',
                                    image=ContentFile(response.content, name=image_name),
                                    is_primary=(idx == 1)
                                )
                                self.stdout.write(self.style.SUCCESS(f'✓ Added gallery image {idx} to {hotel_name}'))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'⚠ Failed to download gallery image for {hotel_name}: {str(e)}'))
                
            except Hotel.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠ Hotel "{hotel_name}" not found'))

        self.stdout.write(self.style.SUCCESS('✓ Finished adding hotel images!'))
