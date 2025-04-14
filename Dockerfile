# Use an official Python runtime as a parent image.
FROM python:3.9-slim

# Set environment variables for non-interactive installations
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install the dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose a port if your app requires it (not necessary for desktop GUIs)
# For GUI applications, you might run the container with proper X11 forwarding.

# Command to run the application.
CMD ["python", "main.py"]
