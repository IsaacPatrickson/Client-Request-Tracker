#!/bin/sh
PORT=${PORT:-8000}

if [ "$DJANGO_ENV" = "production" ]; then
  gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
else
  python manage.py runserver 0.0.0.0:$PORT
fi
