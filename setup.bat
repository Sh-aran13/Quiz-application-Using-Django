@echo off
echo ================================================
echo Quiz Application - Setup Script
echo ================================================
echo.

echo Step 1: Installing Python Dependencies...
pip install -r requirements.txt
echo.

echo Step 2: Creating Database Migrations...
python manage.py makemigrations
echo.

echo Step 3: Applying Migrations...
python manage.py migrate
echo.

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo IMPORTANT: Before running the application:
echo 1. Make sure PostgreSQL is installed and running
echo 2. Create a database named 'quiz_db'
echo 3. Update database password in quiz_project\settings.py
echo.
echo To start the server, run: python manage.py runserver
echo Then visit: http://127.0.0.1:8000/
echo.
pause
