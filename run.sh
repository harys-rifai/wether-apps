#!/bin/bash

# Exit on error
set -e

echo "🌦️ Starting Weather Alert WebApp Build & Run Script..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip and install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations
echo "Running database migrations on Neon PostgreSQL..."
python manage.py migrate

# Check settings integrity
echo "Verifying application check..."
python manage.py check

# Run Django Development Server
echo "Starting Django development server..."
echo "Access the app at: http://127.0.0.1:8000/"
python manage.py runserver
