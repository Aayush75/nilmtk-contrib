# Use a lightweight Python base image
FROM python:3.11-slim

# Install system dependencies for numerical libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source code into image
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install .

# Default command: drop into a shell
CMD ["bash"]
