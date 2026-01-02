#!/bin/bash

echo "🚀 GoExplorer Setup Script"
echo "=========================="
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your credentials."
else
    echo "⚠️  .env file already exists."
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
else
    echo "⚠️  Virtual environment already exists."
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p media/hotels media/buses media/packages media/users media/cities
mkdir -p static/css static/js static/images

# Generate secret key if needed
echo "🔑 Generating Django secret key..."
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Create superuser account:"
python manage.py createsuperuser

# Populate sample cities
echo "🌍 Populating sample cities..."
python manage.py populate_cities

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Edit .env file with your API keys (Razorpay, SendGrid, etc.)"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python manage.py runserver"
echo "4. Visit: http://127.0.0.1:8000"
echo "5. Admin: http://127.0.0.1:8000/admin"
echo ""
echo "🎉 Happy coding!"
