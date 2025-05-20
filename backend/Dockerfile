# Use a base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY . /app

# Expose the port (optional)
EXPOSE 8000

CMD ["sh", "-c", "uvicorn server.api:app --host 0.0.0.0 --port ${PORT:-8000}"]

