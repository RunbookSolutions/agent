# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory to /app
WORKDIR /app

# Copy the package list file into the container
COPY docker-packages.txt .

# Install packages using the package list
RUN apt-get update && \
    xargs -a docker-packages.txt apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./src /app

# Define the command to run your application
CMD [ "python", "/app/main.py" ]