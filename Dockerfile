# Use an official Python runtime as a parent image
FROM python:latest

# Install Required System Tools
RUN apt-get update && \
    apt-get install nmap gcc libkrb5-dev libssl-dev krb5-user -y

# Set the working directory to /app
WORKDIR /app

RUN mkdir plugins,stores

COPY _docker/start.sh /start.sh
RUN chmod +x /start.sh

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY app.py /app
COPY runbooksolutions /app/runbooksolutions

# Define the command to run your application
CMD [ "/start.sh" ]