# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install curl and jq
RUN apt-get update && apt-get install -y curl

# Copy the current directory contents into the container at /app
COPY . /app

# Create a directory for certificates and copy them
RUN mkdir /certificates
COPY certificates/api.coingecko.com.MITM.crt /certificates/
COPY certificates/bylls.com.MITM.crt /certificates/
COPY certificates/customrates.local.MITM.crt /certificates/
COPY certificates/MITM.key /certificates/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 443
EXPOSE 443

# Run app.py with SSL certificate and key
CMD ["python", "app.py"]
