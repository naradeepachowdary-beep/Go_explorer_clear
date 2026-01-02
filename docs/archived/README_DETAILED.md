# GoExplorer - Travel Booking Platform

A comprehensive travel booking platform built with Django, featuring hotel bookings, bus reservations, and holiday packages.

## Features

### Phase 1 - MVP (Admin Driven)
- ✅ Hotel booking system
- ✅ Bus booking system  
- ✅ Holiday packages
- ✅ Django Admin management
- ✅ Complete backend models
- ✅ RESTful APIs

### Phase 2 - Production Ready
- ✅ Responsive UI/UX (Cleartrip-inspired)
- ✅ Razorpay payment integration
- ✅ Email notifications
- ✅ Redis caching
- ✅ Celery task queue
- ⏳ SMS notifications
- ⏳ Advanced search filters
- ⏳ User reviews & ratings

## Tech Stack

- **Backend:** Django 4.2, Django REST Framework
- **Database:** PostgreSQL (production) / SQLite (development)
- **Cache:** Redis
- **Task Queue:** Celery
- **Payment:** Razorpay / Stripe
- **Frontend:** Bootstrap 5, jQuery
- **Email:** SendGrid
- **SMS:** Twilio

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (for production)
- Redis (for caching & celery)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/ravikumar9/Go_explorer_clear.git
cd Go_explorer_clear
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
```bash
cp .env.example .env
# Edit .env file with your credentials
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

Admin Panel: http://127.0.0.1:8000/admin

## Project Structure

```
goexplorer/
├── goexplorer/          # Project settings
├── core/                # Core app (home, cities)
├── hotels/              # Hotel booking
├── buses/               # Bus booking
├── packages/            # Holiday packages
├── bookings/            # Booking management
├── payments/            # Payment processing
├── users/               # User management
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploaded files
└── requirements.txt     # Python dependencies
```

## API Endpoints

### Hotels
- `GET /api/hotels/` - List all hotels
- `GET /api/hotels/<id>/` - Hotel details
- `GET /api/hotels/search/` - Search hotels

### Buses
- `GET /api/buses/search/` - Search buses
- `GET /api/buses/routes/` - List routes
- `GET /api/buses/routes/<id>/` - Route details

### Packages
- `GET /api/packages/` - List packages
- `GET /api/packages/<id>/` - Package details
- `GET /api/packages/search/` - Search packages

### Bookings
- `GET /api/bookings/` - User bookings
- `GET /api/bookings/<booking_id>/` - Booking details

### Payments
- `POST /api/payments/create-order/` - Create payment order
- `POST /api/payments/verify/` - Verify payment

## Admin Panel Usage

1. **Access Admin Panel:** http://127.0.0.1:8000/admin
2. **Add Cities:** Core > Cities
3. **Add Hotels:** Hotels > Hotels
4. **Add Room Types:** Within each hotel
5. **Add Bus Operators:** Buses > Bus Operators
6. **Add Buses:** Buses > Buses
7. **Add Routes:** Buses > Bus Routes
8. **Add Packages:** Packages > Packages

## Configuration

### Razorpay Setup
1. Sign up at https://razorpay.com
2. Get API keys from Dashboard
3. Add to `.env`:
```
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

### Email Setup (SendGrid)
1. Sign up at https://sendgrid.com
2. Create API key
3. Add to `.env`:
```
SENDGRID_API_KEY=your_api_key
DEFAULT_FROM_EMAIL=noreply@goexplorer.in
```

### Redis Setup
```bash
# Install Redis
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                  # macOS

# Start Redis
redis-server
```

### Celery Setup
```bash
# Terminal 1: Start Celery worker
celery -A goexplorer worker -l info

# Terminal 2: Start Celery beat (for scheduled tasks)
celery -A goexplorer beat -l info
```

## Deployment

### Heroku Deployment
```bash
# Install Heroku CLI
heroku login
heroku create goexplorer-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DEBUG=False
heroku config:set RAZORPAY_KEY_ID=your_key

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure PostgreSQL
- [ ] Set up Redis
- [ ] Configure email service
- [ ] Set up SSL certificate
- [ ] Configure domain
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Set up CDN for static files
- [ ] Configure rate limiting

## Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test hotels
python manage.py test bookings
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email support@goexplorer.in or create an issue in the repository.

## Roadmap

### Phase 3 - Advanced Features
- [ ] Flight booking
- [ ] Train booking
- [ ] Cab/taxi booking
- [ ] Multi-language support
- [ ] Mobile apps (iOS/Android)
- [ ] AI-powered recommendations
- [ ] Loyalty program
- [ ] Partner dashboard
- [ ] Advanced analytics
- [ ] Dynamic pricing

## Credits

Developed by GoExplorer Team
Inspired by Cleartrip.com

---

**GoExplorer** - Your Travel Companion 🌍✈️
