from rest_framework import generics, filters
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min, Value, FloatField
from django.db.models.functions import Coalesce
from datetime import date, timedelta
from django.views.decorators.http import require_http_methods
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hotel, RoomType
from .serializers import HotelListSerializer, HotelDetailSerializer, RoomTypeSerializer
from core.models import City


# API Views
class HotelListView(generics.ListAPIView):
    """List all hotels with filters"""
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'star_rating', 'is_featured']
    search_fields = ['name', 'description', 'city__name']
    ordering_fields = ['review_rating', 'name']


class HotelDetailView(generics.RetrieveAPIView):
    """Get hotel details"""
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelDetailSerializer


class HotelSearchView(generics.ListAPIView):
    """Search hotels by city and dates"""
    serializer_class = HotelListSerializer
    
    def get_queryset(self):
        city_id = self.request.query_params.get('city')
        checkin = self.request.query_params.get('checkin')
        checkout = self.request.query_params.get('checkout')
        
        queryset = Hotel.objects.filter(is_active=True)
        
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        
        # Add availability filter based on dates if needed
        
        return queryset


# Web Views (HTML)
def hotel_list(request):
    """Hotel listing page with search"""
    from django.db.models import DecimalField
    
    hotels = Hotel.objects.filter(is_active=True).annotate(
        min_price=Coalesce(Min('room_types__base_price'), Value(0, output_field=DecimalField()))
    )
    cities = City.objects.all().order_by('name')
    
    # Search filters
    city_id = request.GET.get('city_id')
    if city_id:
        hotels = hotels.filter(city_id=city_id)
    
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    star_rating = request.GET.get('star_rating')
    sort = request.GET.get('sort')
    guests = request.GET.get('guests')

    # Basic price range filter (uses annotated min_price)
    if price_min:
        hotels = hotels.filter(min_price__gte=price_min)
    if price_max:
        hotels = hotels.filter(min_price__lte=price_max)

    # Star rating filter
    if star_rating:
        hotels = hotels.filter(star_rating=star_rating)

    # Sorting
    if sort == 'price_asc':
        hotels = hotels.order_by('min_price')
    elif sort == 'price_desc':
        hotels = hotels.order_by('-min_price')
    elif sort == 'rating_desc':
        hotels = hotels.order_by('-review_rating')
    elif sort == 'rating_asc':
        hotels = hotels.order_by('review_rating')
    
    # Convert to list to avoid lazy evaluation issues in template
    hotels = list(hotels)
    
    context = {
        'hotels': hotels,
        'cities': cities,
        'selected_city': city_id,
        'selected_checkin': checkin,
        'selected_checkout': checkout,
        'selected_price_min': price_min,
        'selected_price_max': price_max,
        'selected_star_rating': star_rating,
        'selected_sort': sort,
        'selected_guests': guests,
    }
    
    return render(request, 'hotels/hotel_list.html', context)


def hotel_detail(request, pk):
    """Hotel detail page"""
    hotel = get_object_or_404(Hotel, pk=pk, is_active=True)
    today = date.today()
    default_checkin = request.GET.get('checkin') or today.strftime('%Y-%m-%d')
    default_checkout = request.GET.get('checkout') or (today + timedelta(days=1)).strftime('%Y-%m-%d')
    default_guests = request.GET.get('guests') or 1
    default_room_type = request.GET.get('room_type')
    
    context = {
        'hotel': hotel,
        'prefill_checkin': default_checkin,
        'prefill_checkout': default_checkout,
        'prefill_guests': default_guests,
        'prefill_room_type': default_room_type,
    }
    
    return render(request, 'hotels/hotel_detail.html', context)


def book_hotel(request, pk):
    """Book hotel (POST handler)"""
    hotel = get_object_or_404(Hotel, pk=pk, is_active=True)
    
    if request.method == 'POST':
        # Handle booking
        room_type_id = request.POST.get('room_type')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        num_rooms = int(request.POST.get('num_rooms', 1))
        guest_name = request.POST.get('guest_name')
        guest_email = request.POST.get('guest_email')
        guest_phone = request.POST.get('guest_phone')
        
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        
        # Create booking (simplified)
        from bookings.models import Booking, HotelBooking
        from datetime import datetime
        
        try:
            room_type = RoomType.objects.get(id=room_type_id, hotel=hotel)
            
            # Calculate total
            checkin = datetime.strptime(checkin_date, '%Y-%m-%d').date()
            checkout = datetime.strptime(checkout_date, '%Y-%m-%d').date()
            nights = (checkout - checkin).days
            total = room_type.base_price * nights * num_rooms
            
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                booking_type='hotel',
                total_amount=total,
                status='pending',
                customer_name=guest_name or request.user.get_full_name() or request.user.username,
                customer_email=guest_email or request.user.email,
                customer_phone=guest_phone or getattr(request.user, 'phone', ''),
            )
            
            HotelBooking.objects.create(
                booking=booking,
                room_type=room_type,
                checkin_date=checkin,
                checkout_date=checkout,
                num_rooms=num_rooms,
                guest_name=guest_name,
                guest_email=guest_email,
                guest_phone=guest_phone,
                num_guests=int(request.POST.get('num_guests', 1))
            )
            
            return redirect(f'/bookings/{booking.id}/confirm/')
        except Exception as e:
            return render(request, 'hotels/hotel_detail.html', {
                'hotel': hotel,
                'error': str(e)
            })
    
    return redirect(f'/hotels/{pk}/')
