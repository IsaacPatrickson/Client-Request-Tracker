#!/bin/sh
PORT=${PORT:-8000}

echo "Running migrations..."
python manage.py migrate --noinput

if [ "$DJANGO_ENV" = "production" ]; then
    echo "Starting Gunicorn..."
    gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
else
    echo "Starting Django development server..."
    python manage.py runserver 0.0.0.0:$PORT
fi