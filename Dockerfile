# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Make postinstall.sh executable
RUN chmod +x postinstall.sh

# Run postinstall.sh after installing dependencies
RUN ./postinstall.sh

# Command to run your bot
CMD ["python", "bot.py"]
