# Use the official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY app.py .

# Define the command to run the application using Gunicorn
# Listens on 0.0.0.0 at the port defined by the environment variable PORT
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
