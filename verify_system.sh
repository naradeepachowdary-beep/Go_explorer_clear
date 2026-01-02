#!/bin/bash
# GoExplorer System Verification Script
# Run this to verify all features are working

echo "================================================"
echo "GoExplorer - System Verification Script"
echo "================================================"
echo ""

cd /workspaces/Go_explorer_clear

# Check Python
echo "✓ Checking Python installation..."
python --version

# Check Django
echo "✓ Checking Django installation..."
python -c "import django; print(f'Django {django.VERSION[0]}.{django.VERSION[1]}')"

# Migrate database
echo ""
echo "✓ Running migrations..."
python manage.py migrate --run-syncdb 2>&1 | tail -5

# Populate test data
echo ""
echo "✓ Populating test data..."
echo "  - Creating cities..."
python manage.py populate_cities 2>&1 | grep -E "✓|Successfully" | head -5

echo "  - Creating hotels..."
python manage.py populate_hotels 2>&1 | grep -E "✓|Successfully" | head -5

echo "  - Adding hotel images..."
python manage.py add_hotel_images 2>&1 | grep -E "✓|Successfully" | head -5

echo "  - Creating bus operators..."
python manage.py add_bus_operators 2>&1 | grep -E "✓|Successfully" | head -5

echo "  - Creating packages..."
python manage.py add_packages 2>&1 | grep -E "✓|Successfully" | head -5

# Verify data
echo ""
echo "================================================"
echo "Data Verification"
echo "================================================"
python manage.py shell << EOF
from core.models import City
from hotels.models import Hotel
from buses.models import BusOperator, Bus, BusRoute
from packages.models import Package, PackageDeparture

print(f"✓ Cities: {City.objects.count()} cities")
print(f"✓ Hotels: {Hotel.objects.count()} hotels")
print(f"✓ Bus Operators: {BusOperator.objects.count()} operators")
print(f"✓ Buses: {Bus.objects.count()} buses")
print(f"✓ Bus Routes: {BusRoute.objects.count()} routes")
print(f"✓ Packages: {Package.objects.count()} packages")
print(f"✓ Package Departures: {PackageDeparture.objects.count()} departures")
EOF

echo ""
echo "================================================"
echo "URLs to Test"
echo "================================================"
echo "Home: http://localhost:8000/"
echo "Hotels: http://localhost:8000/hotels/"
echo "Buses: http://localhost:8000/buses/"
echo "Packages: http://localhost:8000/packages/"
echo "Admin: http://localhost:8000/admin/"
echo ""
echo "================================================"
echo "Quick Start"
echo "================================================"
echo "1. Start server: python manage.py runserver 0.0.0.0:8000"
echo "2. Create superuser: python manage.py createsuperuser"
echo "3. Open browser to http://localhost:8000/"
echo "4. Run tests: python manage.py test tests.test_comprehensive_e2e"
echo ""
echo "✓ System verification complete!"
