# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .app_api_streaming/app .

# Install any needed packages specified in requirements.txt
# RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential

RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src

# Expose the port that the application will run on
EXPOSE 5000

# Run the command to start the application
CMD [ "python", "app.py" ]

# docker run -d -p 80:5000 hello_app_prod 
