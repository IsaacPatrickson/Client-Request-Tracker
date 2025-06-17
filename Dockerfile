# Use the official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Collect static files (optional)
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run server (swap to gunicorn for production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
