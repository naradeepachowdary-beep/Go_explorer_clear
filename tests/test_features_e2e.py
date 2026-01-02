"""
Comprehensive End-to-End Feature Tests for GoExplorer
Tests cover:
- Bus booking (mixed gender and ladies-only)
- Package booking
- Property registration
- Operator registration
- API and UI flows
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta, time
from decimal import Decimal
import json

from core.models import City
from buses.models import (
    Bus, BusOperator, BusRoute, BusSchedule, SeatLayout, BusStop,
    BoardingPoint, DroppingPoint
)
from packages.models import Package, PackageDeparture, PackageItinerary
from bookings.models import Booking, BusBooking, BusBookingSeat, PackageBooking
from payments.models import Payment
from property_owners.models import PropertyOwner, Property, PropertyType
from hotels.models import Hotel, RoomType

User = get_user_model()


class BusOperatorRegistrationTestCase(TestCase):
    """Test operator registration and verification flow"""
    
    def test_bus_operator_registration_flow(self):
        """Test complete operator registration"""
        # Create user for operator
        user = User.objects.create_user(
            username='operator1',
            email='operator@test.com',
            password='testpass123',
            phone='+919876543210',
            is_staff=False
        )
        
        # Create operator
        operator = BusOperator.objects.create(
            user=user,
            name='Test Bus Company',
            description='A reliable bus operator',
            contact_phone='+911234567890',
            contact_email='company@test.com',
            business_license='BL123456',
            pan_number='AAAPD1234B',
            gst_number='18AABCT1234H1Z0',
            registered_address='123 Business Street',
            verification_status='pending'
        )
        
        # Verify operator was created
        self.assertEqual(operator.verification_status, 'pending')
        self.assertEqual(operator.user, user)
        
        # Admin verifies operator
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        
        operator.verification_status = 'verified'
        operator.verified_at = timezone.now()
        operator.verified_by = admin_user
        operator.save()
        
        # Check operator is verified
        updated_operator = BusOperator.objects.get(id=operator.id)
        self.assertEqual(updated_operator.verification_status, 'verified')
        self.assertIsNotNone(updated_operator.verified_at)


class BusBookingMixedGenderTestCase(TestCase):
    """Test booking bus with mixed gender passengers"""
    
    def setUp(self):
        self.client = Client()
        # Create cities
        self.city_from = City.objects.create(
            name='Bangalore',
            state='Karnataka',
            country='India',
            code='BNG'
        )
        self.city_to = City.objects.create(
            name='Chennai',
            state='Tamil Nadu',
            country='India',
            code='CHN'
        )
        
        # Create operator
        self.operator_user = User.objects.create_user(
            username='operator_mixed',
            email='op@test.com',
            password='pass123',
            phone='+919876543210'
        )
        
        self.operator = BusOperator.objects.create(
            user=self.operator_user,
            name='Express Buses',
            contact_phone='+911111111111',
            contact_email='express@test.com',
            verification_status='verified'
        )
        
        # Create bus (14 seats for testing)
        self.bus = Bus.objects.create(
            operator=self.operator,
            bus_number='BNG-123',
            bus_name='Express AC Volvo',
            bus_type='volvo',
            total_seats=14,
            manufacturing_year=2022,
            has_ac=True,
            has_wifi=True,
            average_rating=Decimal('4.5')
        )
        
        # Create route
        self.route = BusRoute.objects.create(
            bus=self.bus,
            route_name='Bangalore to Chennai',
            source_city=self.city_from,
            destination_city=self.city_to,
            departure_time=time(14, 0),
            arrival_time=time(20, 0),
            duration_hours=Decimal('6.0'),
            distance_km=Decimal('350'),
            base_fare=Decimal('500')
        )
        
        # Create boarding points
        self.boarding_point = BoardingPoint.objects.create(
            route=self.route,
            name='Bangalore Central',
            address='Downtown, Bangalore',
            city=self.city_from,
            pickup_time=time(14, 0),
            sequence_order=1
        )
        
        # Create dropping point
        self.dropping_point = DroppingPoint.objects.create(
            route=self.route,
            name='Chennai Central',
            address='Downtown, Chennai',
            city=self.city_to,
            drop_time=time(20, 0),
            sequence_order=1
        )
        
        # Create seat layout (7 pairs: 6 general, 1 ladies)
        for row in range(1, 8):  # 7 rows, 2 seats each = 14 seats
            seat_type = 'seater'
            
            # First 6 rows = general, row 7 = ladies
            reserved_for = 'general' if row < 7 else 'ladies'
            
            # Seat A
            SeatLayout.objects.create(
                bus=self.bus,
                seat_number=f'{row}A',
                seat_type=seat_type,
                row=row,
                column=1,
                deck=1,
                reserved_for=reserved_for
            )
            
            # Seat B
            SeatLayout.objects.create(
                bus=self.bus,
                seat_number=f'{row}B',
                seat_type=seat_type,
                row=row,
                column=2,
                deck=1,
                reserved_for=reserved_for
            )
        
        # Create schedule
        travel_date = date.today() + timedelta(days=5)
        self.schedule = BusSchedule.objects.create(
            route=self.route,
            date=travel_date,
            available_seats=14,
            fare=Decimal('500')
        )
        
        # Create test users
        self.user_male = User.objects.create_user(
            username='male_user',
            email='male@test.com',
            password='testpass123',
            phone='+919876543210'
        )
        
        self.user_female = User.objects.create_user(
            username='female_user',
            email='female@test.com',
            password='testpass123',
            phone='+919876543211'
        )
    
    def test_book_bus_mixed_gender_same_transaction(self):
        """Test booking mixed gender passengers in one transaction"""
        self.client.login(username='male_user', password='testpass123')
        
        # Create booking with male and female passengers
        booking = Booking.objects.create(
            user=self.user_male,
            booking_type='bus',
            total_amount=Decimal('1000'),
            status='pending',
            customer_name='Test User',
            customer_email='test@test.com',
            customer_phone='+919876543210'
        )
        
        bus_booking = BusBooking.objects.create(
            booking=booking,
            bus_schedule=self.schedule,
            journey_date=self.schedule.date
        )
        
        # Add male passenger - seat 1A
        seat_1a = SeatLayout.objects.get(seat_number='1A')
        BusBookingSeat.objects.create(
            bus_booking=bus_booking,
            seat=seat_1a,
            passenger_name='John Doe',
            passenger_gender='M',
            passenger_age=30
        )
        
        # Add female passenger - seat 1B
        seat_1b = SeatLayout.objects.get(seat_number='1B')
        BusBookingSeat.objects.create(
            bus_booking=bus_booking,
            seat=seat_1b,
            passenger_name='Jane Doe',
            passenger_gender='F',
            passenger_age=28
        )
        
        # Verify booking was created
        self.assertEqual(BusBookingSeat.objects.filter(bus_booking=bus_booking).count(), 2)
        
        # Get genders
        male_seat = BusBookingSeat.objects.get(passenger_name='John Doe')
        female_seat = BusBookingSeat.objects.get(passenger_name='Jane Doe')
        
        self.assertEqual(male_seat.passenger_gender, 'M')
        self.assertEqual(female_seat.passenger_gender, 'F')
    
    def test_female_and_male_can_book_general_seats(self):
        """Test both males and females can book general seats"""
        # First booking - Male books general seat
        booking1 = Booking.objects.create(
            user=self.user_male,
            booking_type='bus',
            total_amount=Decimal('500'),
            status='confirmed',
            customer_name='Male User',
            customer_email='male@test.com',
            customer_phone='+919876543210'
        )
        
        bus_booking1 = BusBooking.objects.create(
            booking=booking1,
            bus_schedule=self.schedule,
            journey_date=self.schedule.date
        )
        
        # Book general seat (row 1)
        seat_1a = SeatLayout.objects.get(seat_number='1A')
        BusBookingSeat.objects.create(
            bus_booking=bus_booking1,
            seat=seat_1a,
            passenger_name='Male Passenger',
            passenger_gender='M',
            passenger_age=35
        )
        
        # Verify male can book general seat
        self.assertTrue(seat_1a.can_be_booked_by('M'))
        
        # Second booking - Female also books general seat
        booking2 = Booking.objects.create(
            user=self.user_female,
            booking_type='bus',
            total_amount=Decimal('500'),
            status='confirmed',
            customer_name='Female User',
            customer_email='female@test.com',
            customer_phone='+919876543211'
        )
        
        bus_booking2 = BusBooking.objects.create(
            booking=booking2,
            bus_schedule=self.schedule,
            journey_date=self.schedule.date
        )
        
        # Book another general seat (row 2)
        seat_2a = SeatLayout.objects.get(seat_number='2A')
        seat_booking = BusBookingSeat.objects.create(
            bus_booking=bus_booking2,
            seat=seat_2a,
            passenger_name='Female Passenger',
            passenger_gender='F',
            passenger_age=32
        )
        
        # Verify female can also book general seats
        self.assertTrue(seat_2a.can_be_booked_by('F'))
        self.assertEqual(seat_booking.passenger_gender, 'F')


class LadiesOnlyTicketTestCase(TestCase):
    """Test ladies-only seat booking logic"""
    
    def setUp(self):
        self.client = Client()
        
        # Create cities
        self.city_from = City.objects.create(
            name='Delhi',
            state='Delhi',
            country='India',
            code='DEL'
        )
        self.city_to = City.objects.create(
            name='Agra',
            state='Uttar Pradesh',
            country='India',
            code='AGR'
        )
        
        # Create operator
        self.operator_user = User.objects.create_user(
            username='operator_ladies',
            email='ladies_op@test.com',
            password='pass123',
            phone='+919876543220'
        )
        
        self.operator = BusOperator.objects.create(
            user=self.operator_user,
            name='Ladies Safe Buses',
            contact_phone='+911111111112',
            contact_email='ladies@test.com',
            verification_status='verified'
        )
        
        # Create bus (10 seats)
        self.bus = Bus.objects.create(
            operator=self.operator,
            bus_number='DEL-456',
            bus_name='Ladies AC Bus',
            bus_type='ac_seater',
            total_seats=10,
            manufacturing_year=2023,
            has_ac=True,
            average_rating=Decimal('4.8')
        )
        
        # Create route
        self.route = BusRoute.objects.create(
            bus=self.bus,
            route_name='Delhi to Agra',
            source_city=self.city_from,
            destination_city=self.city_to,
            departure_time=time(10, 0),
            arrival_time=time(13, 0),
            duration_hours=Decimal('3.0'),
            distance_km=Decimal('206'),
            base_fare=Decimal('400')
        )
        
        # Create boarding and dropping points
        self.boarding_point = BoardingPoint.objects.create(
            route=self.route,
            name='Delhi Railway Station',
            address='New Delhi',
            city=self.city_from,
            pickup_time=time(10, 0),
            sequence_order=1
        )
        
        self.dropping_point = DroppingPoint.objects.create(
            route=self.route,
            name='Agra Fort',
            address='Agra',
            city=self.city_to,
            drop_time=time(13, 0),
            sequence_order=1
        )
        
        # Create seat layout (5 ladies, 5 general)
        for row in range(1, 6):
            # Seat A = ladies, Seat B = general
            SeatLayout.objects.create(
                bus=self.bus,
                seat_number=f'{row}A',
                seat_type='seater',
                row=row,
                column=1,
                deck=1,
                reserved_for='ladies'
            )
            
            SeatLayout.objects.create(
                bus=self.bus,
                seat_number=f'{row}B',
                seat_type='seater',
                row=row,
                column=2,
                deck=1,
                reserved_for='general'
            )
        
        # Create schedule
        travel_date = date.today() + timedelta(days=3)
        self.schedule = BusSchedule.objects.create(
            route=self.route,
            date=travel_date,
            available_seats=10,
            fare=Decimal('400')
        )
        
        # Create test users
        self.female_user = User.objects.create_user(
            username='female1',
            email='female1@test.com',
            password='testpass123',
            phone='+919999999999'
        )
        
        self.male_user = User.objects.create_user(
            username='male1',
            email='male1@test.com',
            password='testpass123',
            phone='+918888888888'
        )
    
    def test_only_females_can_book_ladies_seats(self):
        """Test that only females can book ladies seats"""
        # Female books ladies seat
        booking_female = Booking.objects.create(
            user=self.female_user,
            booking_type='bus',
            total_amount=Decimal('400'),
            status='confirmed',
            customer_name='Female User',
            customer_email='female@test.com',
            customer_phone='+919999999999'
        )
        
        bus_booking_female = BusBooking.objects.create(
            booking=booking_female,
            bus_schedule=self.schedule,
            journey_date=self.schedule.date
        )
        
        seat_1a = SeatLayout.objects.get(seat_number='1A')
        
        # Verify female can book ladies seat
        self.assertTrue(seat_1a.can_be_booked_by('F'))
        
        seat_booking = BusBookingSeat.objects.create(
            bus_booking=bus_booking_female,
            seat=seat_1a,
            passenger_name='Priya Kumar',
            passenger_gender='F',
            passenger_age=25
        )
        
        self.assertEqual(seat_booking.passenger_gender, 'F')
        
        # Male should NOT be able to book ladies seat
        self.assertFalse(seat_1a.can_be_booked_by('M'))
    
    def test_female_can_book_general_seat(self):
        """Test that females can also book general seats"""
        booking = Booking.objects.create(
            user=self.female_user,
            booking_type='bus',
            total_amount=Decimal('400'),
            status='confirmed',
            customer_name='Female User',
            customer_email='female@test.com',
            customer_phone='+919999999999'
        )
        
        bus_booking = BusBooking.objects.create(
            booking=booking,
            bus_schedule=self.schedule,
            journey_date=self.schedule.date
        )
        
        seat_1b = SeatLayout.objects.get(seat_number='1B')  # General seat
        
        # Verify seat is general
        self.assertTrue(seat_1b.can_be_booked_by('F'))
        
        seat_booking = BusBookingSeat.objects.create(
            bus_booking=bus_booking,
            seat=seat_1b,
            passenger_name='Anjali Sharma',
            passenger_gender='F',
            passenger_age=28
        )
        
        self.assertEqual(seat_booking.passenger_gender, 'F')
    
    def test_multiple_females_can_book_ladies_seats(self):
        """Test that multiple females can book ladies seats"""
        # First female booking
        booking1 = Booking.objects.create(
            user=self.female_user,
            booking_type='bus',
            total_amount=Decimal('400'),
            status='confirmed',
            customer_name='Female 1',
            customer_email='female1@test.com',
            customer_phone='+919999999999'
        )
        
        bus_booking1 = BusBooking.objects.create(
            booking=booking1,
            bus_schedule=self.schedule,
            journey_date=self.schedule.date
        )
        
        seat_1a = SeatLayout.objects.get(seat_number='1A')
        BusBookingSeat.objects.create(
            bus_booking=bus_booking1,
            seat=seat_1a,
            passenger_name='Female Passenger 1',
            passenger_gender='F',
            passenger_age=26
        )
        
        # Second female can also book ladies seat
        female_user2 = User.objects.create_user(
            username='female2',
            email='female2@test.com',
            password='testpass123',
            phone='+918888888889'
        )
        
        booking2 = Booking.objects.create(
            user=female_user2,
            booking_type='bus',
            total_amount=Decimal('400'),
            status='confirmed',
            customer_name='Female 2',
            customer_email='female2@test.com',
            customer_phone='+918888888889'
        )
        
        bus_booking2 = BusBooking.objects.create(
            booking=booking2,
            bus_schedule=self.schedule,
            journey_date=self.schedule.date
        )
        
        seat_2a = SeatLayout.objects.get(seat_number='2A')
        seat_booking = BusBookingSeat.objects.create(
            bus_booking=bus_booking2,
            seat=seat_2a,
            passenger_name='Female Passenger 2',
            passenger_gender='F',
            passenger_age=29
        )
        
        # Verify both can book ladies seats
        self.assertTrue(seat_2a.can_be_booked_by('F'))
        self.assertEqual(seat_booking.passenger_gender, 'F')


class PackageBookingTestCase(TestCase):
    """Test package booking functionality"""
    
    def setUp(self):
        self.client = Client()
        
        # Create cities
        self.source = City.objects.create(
            name='Mumbai',
            state='Maharashtra',
            country='India',
            code='MUM'
        )
        self.destination = City.objects.create(
            name='Goa',
            state='Goa',
            country='India',
            code='GOA'
        )
        
        # Create package
        self.package = Package.objects.create(
            name='Goa Beach Getaway',
            description='3 days in beautiful Goa',
            package_type='beach',
            duration_days=3,
            duration_nights=2,
            starting_price=Decimal('15000'),
            is_featured=True
        )
        
        # Add destination cities
        self.package.destination_cities.add(self.destination)
        
        # Create itinerary
        PackageItinerary.objects.create(
            package=self.package,
            day_number=1,
            title='Arrival and Beach Visit',
            description='Arrive in Goa, visit Baga Beach',
            activities='Beach, Sunset'
        )
        
        PackageItinerary.objects.create(
            package=self.package,
            day_number=2,
            title='Water Sports',
            description='Water sports activities',
            activities='Water skiing, Jet ski'
        )
        
        PackageItinerary.objects.create(
            package=self.package,
            day_number=3,
            title='Departure',
            description='Departure day',
            activities='Shopping, Local market'
        )
        
        # Create package departure
        departure_date = date.today() + timedelta(days=10)
        return_date = departure_date + timedelta(days=3)
        self.departure = PackageDeparture.objects.create(
            package=self.package,
            departure_date=departure_date,
            return_date=return_date,
            available_slots=20,
            price_per_person=Decimal('13500')
        )
        
        # Create test user
        self.user = User.objects.create_user(
            username='package_user',
            email='package@test.com',
            password='testpass123',
            phone='+917777777777'
        )
    
    def test_package_booking_flow(self):
        """Test complete package booking"""
        self.client.login(username='package_user', password='testpass123')
        
        # Create booking
        booking = Booking.objects.create(
            user=self.user,
            booking_type='package',
            total_amount=self.departure.price_per_person * 2,
            status='pending',
            customer_name='Test User',
            customer_email='package@test.com',
            customer_phone='+917777777777'
        )
        
        # Create package booking
        package_booking = PackageBooking.objects.create(
            booking=booking,
            package_departure=self.departure,
            number_of_travelers=2
        )
        
        # Verify booking created
        self.assertEqual(package_booking.package_departure, self.departure)
        self.assertEqual(package_booking.number_of_travelers, 2)
    
    def test_package_list_and_search(self):
        """Test package listing and search"""
        # Create another package
        package2 = Package.objects.create(
            name='Manali Hill Station',
            description='Adventure in mountains',
            package_type='adventure',
            duration_days=5,
            duration_nights=4,
            starting_price=Decimal('20000')
        )
        
        manali = City.objects.create(
            name='Manali',
            state='Himachal Pradesh',
            country='India',
            code='MNL'
        )
        package2.destination_cities.add(manali)
        
        # Get all packages
        packages = Package.objects.all()
        self.assertEqual(packages.count(), 2)
        
        # Search by destination city
        goa_packages = Package.objects.filter(destination_cities__name='Goa')
        self.assertEqual(goa_packages.count(), 1)
        self.assertEqual(goa_packages.first().name, 'Goa Beach Getaway')


class PropertyOwnerRegistrationTestCase(TestCase):
    """Test property owner and property registration"""
    
    def setUp(self):
        self.client = Client()
        
        # Create property type
        self.property_type = PropertyType.objects.create(
            name='homestay',
            description='Commercial hotel property'
        )
        
        # Create city
        self.city = City.objects.create(
            name='Pune',
            state='Maharashtra',
            country='India',
            code='PUN'
        )
    
    def test_property_owner_registration(self):
        """Test property owner registration flow"""
        # Create user
        owner_user = User.objects.create_user(
            username='property_owner',
            email='owner@test.com',
            password='testpass123',
            phone='+916666666666'
        )
        
        # Create property owner
        owner = PropertyOwner.objects.create(
            user=owner_user,
            business_name='Heritage Hotels',
            property_type=self.property_type,
            description='Luxury heritage properties',
            owner_name='Mr. Sharma',
            owner_phone='+911111111113',
            owner_email='heritage@test.com',
            city=self.city,
            address='123 Main Street, Pune',
            pincode='411001',
            pan_number='AAAPD9999B',
            gst_number='27AABCT1234H1Z0',
            verification_status='pending'
        )
        
        # Verify owner created
        self.assertEqual(owner.verification_status, 'pending')
        self.assertEqual(owner.user, owner_user)
        self.assertEqual(owner.business_name, 'Heritage Hotels')
    
    def test_property_registration(self):
        """Test property registration under property owner"""
        # Create owner
        owner_user = User.objects.create_user(
            username='owner2',
            email='owner2@test.com',
            password='testpass123',
            phone='+916666666667'
        )
        
        owner = PropertyOwner.objects.create(
            user=owner_user,
            business_name='Luxury Estates',
            property_type=self.property_type,
            description='Luxury property management',
            owner_name='Ms. Patel',
            owner_phone='+911111111114',
            owner_email='luxury@test.com',
            city=self.city,
            address='456 Business Ave, Pune',
            pincode='411002',
            verification_status='verified'
        )
        
        # Create property
        property_obj = Property.objects.create(
            owner=owner,
            name='Grand Pune Hotel',
            description='5-star luxury hotel in Pune',
            amenities='WiFi, AC, TV, Restaurant, Parking',
            base_price=Decimal('5000'),
            max_guests=4,
            num_bedrooms=2,
            num_bathrooms=2
        )
        
        # Verify property created
        self.assertEqual(property_obj.owner, owner)
        self.assertEqual(property_obj.name, 'Grand Pune Hotel')
        self.assertEqual(property_obj.max_guests, 4)


class IntegrationTestAllFeatures(TestCase):
    """Integration test covering all features"""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_user_journey(self):
        """Test complete user journey: register -> book bus -> book package"""
        # 1. User registration
        user = User.objects.create_user(
            username='journey_user',
            email='journey@test.com',
            password='testpass123',
            phone='+915555555555',
            first_name='Test',
            last_name='User'
        )
        
        # 2. User logs in
        login_result = self.client.login(
            username='journey_user',
            password='testpass123'
        )
        self.assertTrue(login_result)
        
        # 3. Create bus booking
        city1 = City.objects.create(
            name='Hyderabad',
            state='Telangana',
            country='India',
            code='HYD'
        )
        city2 = City.objects.create(
            name='Bangalore',
            state='Karnataka',
            country='India',
            code='BNG'
        )
        
        operator = BusOperator.objects.create(
            name='Premium Travels',
            contact_phone='+911111111115',
            contact_email='premium@test.com',
            verification_status='verified'
        )
        
        bus = Bus.objects.create(
            operator=operator,
            bus_number='HYD-789',
            bus_name='Premium Volvo',
            bus_type='volvo',
            total_seats=45,
            manufacturing_year=2023,
            has_ac=True,
            average_rating=Decimal('4.6')
        )
        
        route = BusRoute.objects.create(
            bus=bus,
            route_name='Hyderabad to Bangalore',
            source_city=city1,
            destination_city=city2,
            departure_time=time(18, 0),
            arrival_time=time(23, 30),
            duration_hours=Decimal('5.5'),
            distance_km=Decimal('575'),
            base_fare=Decimal('600')
        )
        
        schedule = BusSchedule.objects.create(
            route=route,
            date=date.today() + timedelta(days=7),
            available_seats=45,
            fare=Decimal('600')
        )
        
        boarding = BoardingPoint.objects.create(
            route=route,
            name='Hyderabad Bus Stand',
            address='Hyderabad',
            city=city1,
            pickup_time=time(18, 0),
            sequence_order=1
        )
        
        dropping = DroppingPoint.objects.create(
            route=route,
            name='Bangalore Bus Stand',
            address='Bangalore',
            city=city2,
            drop_time=time(23, 30),
            sequence_order=1
        )
        
        # Create seats
        for i in range(1, 46):
            row = (i - 1) // 2 + 1
            col = (i - 1) % 2 + 1
            SeatLayout.objects.create(
                bus=bus,
                seat_number=f'{row}{chr(64+col)}',
                seat_type='seater',
                row=row,
                column=col,
                deck=1,
                reserved_for='general'
            )
        
        # Book bus
        bus_booking = Booking.objects.create(
            user=user,
            booking_type='bus',
            total_amount=Decimal('600'),
            status='confirmed',
            customer_name='Test User',
            customer_email='journey@test.com',
            customer_phone='+915555555555'
        )
        
        bus_booking_detail = BusBooking.objects.create(
            booking=bus_booking,
            bus_schedule=schedule,
            journey_date=schedule.date
        )
        
        seat = SeatLayout.objects.first()
        BusBookingSeat.objects.create(
            bus_booking=bus_booking_detail,
            seat=seat,
            passenger_name='Test User',
            passenger_gender='M',
            passenger_age=30
        )
        
        # Verify bus booking created
        self.assertEqual(Booking.objects.filter(user=user, booking_type='bus').count(), 1)
        
        # 4. Create package booking
        package = Package.objects.create(
            name='Kerala Backwaters',
            description='Experience Kerala',
            package_type='beach',
            duration_days=4,
            duration_nights=3,
            starting_price=Decimal('25000')
        )
        
        kochi = City.objects.create(
            name='Kochi',
            state='Kerala',
            country='India',
            code='KCH'
        )
        package.destination_cities.add(kochi)
        
        departure_dt = date.today() + timedelta(days=14)
        return_dt = departure_dt + timedelta(days=3)
        departure = PackageDeparture.objects.create(
            package=package,
            departure_date=departure_dt,
            return_date=return_dt,
            available_slots=30,
            price_per_person=Decimal('21250')
        )
        
        package_booking = Booking.objects.create(
            user=user,
            booking_type='package',
            total_amount=departure.price_per_person * 2,
            status='confirmed',
            customer_name='Test User',
            customer_email='journey@test.com',
            customer_phone='+915555555555'
        )
        
        PackageBooking.objects.create(
            booking=package_booking,
            package_departure=departure,
            number_of_travelers=2
        )
        
        # Verify package booking created
        self.assertEqual(Booking.objects.filter(user=user, booking_type='package').count(), 1)
        
        # 5. Verify user has both bookings
        user_bookings = Booking.objects.filter(user=user)
        self.assertEqual(user_bookings.count(), 2)
        
        booking_types = set(user_bookings.values_list('booking_type', flat=True))
        self.assertIn('bus', booking_types)
        self.assertIn('package', booking_types)
