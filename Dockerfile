# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install curl and jq
RUN apt-get update && apt-get install -y curl jq

# Copy the current directory contents into the container at /app
COPY . /app

# Create a directory for certificates and copy them
RUN mkdir /certificates
COPY certificates/api.coingecko.com.MITM.crt /certificates/
COPY certificates/api.coingecko.com.MITM.key /certificates/

# Run the curl and jq commands to fetch and process data
RUN curl https://api.coingecko.com/api/v3/exchange_rates > /tmp/exchange_rates.json
RUN cat /tmp/exchange_rates.json | jq '.rates |= with_entries(if .value.type == "fiat" then .value.value *= 10 else . end)' > /tmp/exchange_rates_10x.json

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 443
EXPOSE 443

# Run app.py with SSL certificate and key
CMD ["python", "app.py"]
