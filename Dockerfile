# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies in one step
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Use a non-root user for security (optional, if applicable)
# RUN useradd -m appuser && chown -R appuser /usr/src/app
# USER appuser
