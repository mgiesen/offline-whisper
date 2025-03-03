# Base image with Python 3.9
FROM python:3.9-slim

# System dependencies for Whisper
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create temporary directory
RUN mkdir -p /tmp

# Copy application code
COPY main.py .

# Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8076"]
