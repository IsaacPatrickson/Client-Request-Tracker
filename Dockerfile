# Use official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Django will use
EXPOSE 8000

# Copy entrypoint script and make sure it is executable
COPY entrypoint.sh /app/entrypoint.sh
COPY render-predeploy.sh /app/render-predeploy.sh
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/render-predeploy.sh

# Use entrypoint to start the server
CMD ["/app/entrypoint.sh"]