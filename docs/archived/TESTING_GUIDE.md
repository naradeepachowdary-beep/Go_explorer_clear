# GoExplorer - Testing & Usage Guide

## 🚀 Quick Start (Step-by-Step)

### Step 1: Initial Setup

```bash
# Navigate to project directory
cd /workspaces/Go_explorer_clear

# Option A: Automated Setup (Recommended)
chmod +x setup.sh
./setup.sh

# Option B: Manual Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_cities
```

### Step 2: Start the Development Server

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the server
python manage.py runserver
```

**Access Points:**
- Homepage: http://127.0.0.1:8000
- Admin Panel: http://127.0.0.1:8000/admin

---

## 📋 Admin Panel Testing Guide

### Login to Admin
1. Go to http://127.0.0.1:8000/admin
2. Use the superuser credentials you created
3. You'll see the GoExplorer Admin Dashboard

### Test Scenario 1: Add a Hotel

**Step 1: Add a City (if not already done)**
1. Click on "Cities" under CORE
2. Click "Add City"
3. Fill in:
   - Name: Mumbai
   - State: Maharashtra
   - Country: India
   - Code: BOM
   - Is Popular: ✓
4. Click "Save"

**Step 2: Add a Hotel**
1. Click on "Hotels" under HOTELS
2. Click "Add Hotel"
3. Fill in basic info:
   - Name: Taj Mahal Palace
   - Description: Luxury heritage hotel in Mumbai
   - City: Mumbai (select from dropdown)
   - Address: Apollo Bunder, Colaba
   - Star Rating: 5
   - Review Rating: 4.8
   - Contact Phone: +91-22-66653366
   - Contact Email: info@tajhotels.com
4. Check amenities:
   - WiFi: ✓
   - Parking: ✓
   - Pool: ✓
   - Gym: ✓
   - Restaurant: ✓
   - Spa: ✓
   - AC: ✓
5. Set timings:
   - Check-in: 14:00
   - Check-out: 11:00
6. Mark as Featured: ✓
7. Mark as Active: ✓

**Step 3: Add Room Type (inline)**
1. In the same form, scroll to "Room types" section
2. Click "Add another Room type"
3. Fill in:
   - Name: Deluxe Room
   - Room Type: Deluxe
   - Description: Spacious room with city view
   - Max Occupancy: 2
   - Number of Beds: 1
   - Base Price: 15000
   - Total Rooms: 20
   - Is Available: ✓
4. Click "Save and continue editing" or "Save"

### Test Scenario 2: Add a Bus Service

**Step 1: Add Bus Operator**
1. Go to "Bus operators" under BUSES
2. Click "Add Bus operator"
3. Fill in:
   - Name: VRL Travels
   - Description: Premium bus service
   - Contact Phone: +91-80-12345678
   - Contact Email: info@vrltravels.com
   - Rating: 4.5
   - Is Active: ✓
4. Save

**Step 2: Add a Bus**
1. Go to "Buses" under BUSES
2. Click "Add Bus"
3. Fill in:
   - Operator: VRL Travels
   - Bus Number: KA01AB1234
   - Bus Name: VRL Luxury
   - Bus Type: AC Sleeper
   - Total Seats: 40
4. Check amenities:
   - AC: ✓
   - WiFi: ✓
   - Charging Point: ✓
   - Blanket: ✓
   - Water Bottle: ✓
5. Is Active: ✓
6. Save

**Step 3: Add Route**
1. Go to "Bus routes" under BUSES
2. Click "Add Bus route"
3. Fill in:
   - Bus: VRL Luxury (KA01AB1234)
   - Route Name: Bangalore to Mumbai Express
   - Source City: Bangalore
   - Destination City: Mumbai
   - Departure Time: 20:00
   - Arrival Time: 08:00
   - Duration Hours: 12
   - Distance: 850 km
   - Base Fare: 1500
   - Check all operation days
   - Is Active: ✓
4. Save

**Step 4: Add Schedule**
1. Go to "Bus schedules" under BUSES
2. Click "Add Bus schedule"
3. Fill in:
   - Route: Bangalore to Mumbai Express
   - Date: Tomorrow's date
   - Available Seats: 40
   - Fare: 1500
   - Is Active: ✓
4. Save

### Test Scenario 3: Add Holiday Package

**Step 1: Create Package**
1. Go to "Packages" under PACKAGES
2. Click "Add Package"
3. Fill in:
   - Name: Goa Beach Getaway
   - Description: 5-day beach vacation
   - Package Type: Beach
   - Destination Cities: Select Goa
   - Duration Days: 5
   - Duration Nights: 4
   - Starting Price: 15000
   - Check inclusions:
     - Hotel: ✓
     - Transport: ✓
     - Meals: ✓
     - Sightseeing: ✓
   - Meal Plan:
     - Breakfast: ✓
     - Dinner: ✓
   - Min Group Size: 2
   - Max Group Size: 20
   - Rating: 4.7
   - Is Featured: ✓
   - Is Active: ✓

**Step 2: Add Itinerary (inline)**
1. In "Package itinerary" section
2. Add Day 1:
   - Day Number: 1
   - Title: Arrival & Beach Visit
   - Description: Check-in and relax at Baga Beach
   - Activities: Swimming, Beach Sports
   - Meals Included: Dinner
   - Accommodation: Beach Resort
3. Add more days similarly

**Step 3: Add Departure**
1. In "Package departures" section
2. Add:
   - Departure Date: Next month
   - Return Date: 5 days later
   - Available Slots: 20
   - Price Per Person: 15000
   - Is Active: ✓
3. Save

---

## 🌐 Frontend Testing

### Test Homepage
1. Visit http://127.0.0.1:8000
2. You should see:
   - Hero section with search forms
   - Tabs for Hotels, Buses, Packages
   - Featured hotels (if you added any)
   - Popular packages

### Test Hotel Search
1. On homepage, select "Hotels" tab
2. Select a city
3. Choose check-in and check-out dates
4. Click "Search Hotels"
5. You'll be redirected to API endpoint showing JSON results

### Test Bus Search
1. Select "Buses" tab
2. Choose source and destination
3. Select journey date
4. Click "Search Buses"
5. View results

### Test Package Search
1. Select "Packages" tab
2. Choose package type
3. Enter duration
4. Click "Search Packages"
5. View results

---

## 🧪 API Testing

### Using Browser
Simply visit these URLs:

**Hotels:**
- List: http://127.0.0.1:8000/api/hotels/
- Search: http://127.0.0.1:8000/api/hotels/search/?city=1
- Detail: http://127.0.0.1:8000/api/hotels/1/

**Buses:**
- Search: http://127.0.0.1:8000/api/buses/search/?source=1&destination=2&date=2024-02-01
- Routes: http://127.0.0.1:8000/api/buses/routes/

**Packages:**
- List: http://127.0.0.1:8000/api/packages/
- Search: http://127.0.0.1:8000/api/packages/search/?type=beach
- Detail: http://127.0.0.1:8000/api/packages/1/

### Using cURL

```bash
# List all hotels
curl http://127.0.0.1:8000/api/hotels/

# Search hotels in a city
curl "http://127.0.0.1:8000/api/hotels/search/?city=1&checkin=2024-02-01&checkout=2024-02-05"

# Get hotel details
curl http://127.0.0.1:8000/api/hotels/1/

# Search buses
curl "http://127.0.0.1:8000/api/buses/search/?source=1&destination=2&date=2024-02-01"

# List packages
curl http://127.0.0.1:8000/api/packages/

# Search packages
curl "http://127.0.0.1:8000/api/packages/search/?type=beach&min_price=10000&max_price=20000"
```

---

## 💳 Payment Testing

### Setup Razorpay Test Mode

1. Go to https://razorpay.com
2. Sign up for free account
3. In Dashboard, enable Test Mode
4. Go to Settings > API Keys
5. Copy "Test Key ID" and "Test Key Secret"
6. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=rzp_test_xxxxx
   RAZORPAY_KEY_SECRET=xxxxx
   ```
7. Restart server

### Test Payment Flow

**Note:** Full payment testing requires authentication. For now, you can test the API endpoints in admin.

Test Cards for Razorpay:
- Success: 4111 1111 1111 1111
- Failure: 4012 8888 8888 1881
- CVV: Any 3 digits
- Expiry: Any future date
- OTP: 000000

---

## 📧 Email Testing (Optional)

### Using Console Backend (Default)
Emails are printed to console by default for testing.

### Using SendGrid (Production)
1. Sign up at https://sendgrid.com
2. Create API key
3. Add to `.env`:
   ```
   SENDGRID_API_KEY=SG.xxxxx
   DEFAULT_FROM_EMAIL=noreply@goexplorer.in
   ```
4. Restart server

---

## 🔧 Common Tasks

### Create Sample Bookings (via Django Shell)

```bash
python manage.py shell
```

```python
from users.models import User
from bookings.models import Booking, HotelBooking
from hotels.models import RoomType
from datetime import date

# Get user
user = User.objects.first()

# Get room type
room = RoomType.objects.first()

# Create booking
booking = Booking.objects.create(
    user=user,
    booking_type='hotel',
    status='confirmed',
    total_amount=15000,
    paid_amount=15000,
    customer_name='Test User',
    customer_email='test@example.com',
    customer_phone='+919876543210'
)

# Create hotel booking details
hotel_booking = HotelBooking.objects.create(
    booking=booking,
    room_type=room,
    check_in=date(2024, 2, 1),
    check_out=date(2024, 2, 5),
    number_of_rooms=1,
    number_of_adults=2,
    total_nights=4
)

print(f"Booking created: {booking.booking_id}")
```

### View All Data

```bash
python manage.py shell
```

```python
from core.models import City
from hotels.models import Hotel
from buses.models import Bus
from packages.models import Package

print(f"Cities: {City.objects.count()}")
print(f"Hotels: {Hotel.objects.count()}")
print(f"Buses: {Bus.objects.count()}")
print(f"Packages: {Package.objects.count()}")
```

---

## 🐛 Troubleshooting

### Issue: Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Issue: Database errors
```bash
python manage.py migrate
```

### Issue: Admin login not working
```bash
python manage.py createsuperuser
```

### Issue: Module not found
```bash
pip install -r requirements.txt
```

---

## ✅ Production Checklist

Before going live:

1. **Environment Setup**
   - [ ] Set `DEBUG=False` in `.env`
   - [ ] Generate new `SECRET_KEY`
   - [ ] Configure `ALLOWED_HOSTS`
   - [ ] Set up PostgreSQL database
   - [ ] Configure Redis

2. **Payment Gateway**
   - [ ] Get production Razorpay keys
   - [ ] Add live mode keys to `.env`
   - [ ] Test with real cards in staging

3. **Email Service**
   - [ ] Set up SendGrid production account
   - [ ] Verify domain
   - [ ] Configure DNS records

4. **Domain & Hosting**
   - [ ] Purchase domain (goexplorer.in)
   - [ ] Set up hosting (Heroku/AWS/DigitalOcean)
   - [ ] Configure DNS
   - [ ] Set up SSL certificate

5. **Content**
   - [ ] Add real hotels, buses, packages
   - [ ] Upload high-quality images
   - [ ] Write compelling descriptions
   - [ ] Set up pricing strategy

6. **Testing**
   - [ ] Test all booking flows
   - [ ] Test payment processing
   - [ ] Test email notifications
   - [ ] Mobile responsiveness check

7. **Legal & Compliance**
   - [ ] Terms & Conditions
   - [ ] Privacy Policy
   - [ ] Refund Policy
   - [ ] GST registration (if applicable)

---

## 📞 Need Help?

- **Documentation**: Check README_DETAILED.md
- **API Reference**: See API_DOCUMENTATION.md
- **Deployment**: Read DEPLOYMENT.md
- **Email**: support@goexplorer.in

---

## 🎉 Success Indicators

You've successfully set up GoExplorer if:
- ✅ Admin panel is accessible and working
- ✅ You can add hotels, buses, packages
- ✅ Homepage loads with search forms
- ✅ API endpoints return data
- ✅ No error messages in terminal

---

**Happy Testing! 🚀**
