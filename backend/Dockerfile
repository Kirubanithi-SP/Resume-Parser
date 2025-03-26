# Use an official Python runtime as a parent image
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use a minimal base image for production
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Make port 443 available to the outside world
EXPOSE 443

# Run the application using Flask's built-in server
CMD ["flask", "run", "--host=0.0.0.0", "--port=443"]