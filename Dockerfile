# Use the official Python 3.10 slim image (or 3.9 if you want)
FROM python:3.10-slim

# Install system dependencies needed for building aiohttp and other libs
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all other files
COPY . .

# Command to run your bot
CMD ["python", "bot.py"]
