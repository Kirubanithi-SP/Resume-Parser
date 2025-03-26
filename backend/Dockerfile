# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Create requirements.txt if you haven't already with `pip freeze > requirements.txt`
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
# Azure App Service typically uses port 80 or 8080
EXPOSE 443

# Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application using gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:443", "app:app"]