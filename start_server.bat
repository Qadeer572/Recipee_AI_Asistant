@echo off
echo ========================================
echo Recipe AI Assistant - Django Web App
echo ========================================
echo.
echo Starting Django development server...
echo.
echo Open your browser and go to:
echo http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

poetry run python manage.py runserver
