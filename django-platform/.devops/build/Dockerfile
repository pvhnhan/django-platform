# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 8000 for the Django app
EXPOSE 8000

# Define environment variable
ENV NAME prod

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]