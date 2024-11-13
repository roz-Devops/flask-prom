# Use the official Python image as a base
FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install Flask prometheus_client Response Counter mysql-connector-python

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
