@echo off
echo 🚀 GoExplorer Setup Script
echo ==========================
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your credentials.
) else (
    echo ⚠️  .env file already exists.
)

REM Create virtual environment
if not exist venv (
    echo 🐍 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created.
) else (
    echo ⚠️  Virtual environment already exists.
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create necessary directories
echo 📁 Creating directories...
mkdir logs 2>nul
mkdir media\hotels media\buses media\packages media\users media\cities 2>nul
mkdir static\css static\js static\images 2>nul

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo 👤 Create superuser account:
python manage.py createsuperuser

REM Populate sample cities
echo 🌍 Populating sample cities...
python manage.py populate_cities

REM Collect static files
echo 📦 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ✅ Setup complete!
echo.
echo 📚 Next steps:
echo 1. Edit .env file with your API keys (Razorpay, SendGrid, etc.)
echo 2. Run: venv\Scripts\activate
echo 3. Run: python manage.py runserver
echo 4. Visit: http://127.0.0.1:8000
echo 5. Admin: http://127.0.0.1:8000/admin
echo.
echo 🎉 Happy coding!
pause
