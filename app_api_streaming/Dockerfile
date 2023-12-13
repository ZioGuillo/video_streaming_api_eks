# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app .

# Update and upgrade system packages
RUN apt-get update && apt-get -y upgrade && apt-get -y install \
    nginx \
    python3-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src

# Expose the port that the application will run on
EXPOSE 5000

# Run the command to start the application
CMD [ "python", "app.py" ]