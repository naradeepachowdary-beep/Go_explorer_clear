#!/bin/bash

# GoExplorer Quick Start Script
# This script starts the Django development server

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start the server
echo "🚀 Starting GoExplorer..."
echo "📍 Server will be available at: http://localhost:8000/"
echo "👤 Admin panel: http://localhost:8000/admin/"
echo "🔑 Admin credentials: admin / admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver 0.0.0.0:8000
