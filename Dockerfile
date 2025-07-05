# Use official Python image
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Pre‑create dir for WhiteNoise
RUN mkdir -p /app/staticfiles

# Collect static files *at build time*
RUN python manage.py collectstatic --noinput

# Ensure entrypoint scripts are executable
RUN chmod +x /app/entrypoint.sh /app/render-predeploy.sh

EXPOSE 8000

# Start the app
CMD ["/app/entrypoint.sh"]
