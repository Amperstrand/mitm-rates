from flask import jsonify, request, send_from_directory
import requests
import os
import json

def get_price_from_coingecko():
    coingecko_10x_output_file_path = '/tmp/exchange_rates_10x.json'
    if not os.path.exists(coingecko_10x_output_file_path):
        # Fetch exchange rates data
        url = "https://api.coingecko.com/api/v3/exchange_rates"
        response = requests.get(url)
        exchange_rates = response.json()

        # Process the data
        for key, value in exchange_rates['rates'].items():
            if value['type'] == "fiat":
                value['value'] *= 10

        # Save the processed data to a file
        with open(coingecko_10x_output_file_path, 'w') as output_file:
            json.dump(exchange_rates, output_file, indent=4)

        print("Data from coingecko fetched and processed successfully.")


    else:
        print(f"{coingecko_10x_output_file_path} already exists. Skipping data fetch and processing.")


    return send_from_directory('/tmp', 'exchange_rates_10x.json')

def get_price_from_bitbank():
    bitbank_output_file_path = '/tmp/bitbank.json'
    if not os.path.exists(bitbank_output_file_path):
        # Fetch exchange rates data
        url = "https://public.bitbank.cc/tickers"
        response = requests.get(url)
        exchange_rates = response.json()

        # Process the data
        #for key, value in exchange_rates['rates'].items():
        #    if value['type'] == "fiat":
        #        value['value'] *= 10

        # Save the processed data to a file
        with open(bitbank_output_file_path, 'w') as bitbank_output_file_path:
            json.dump(exchange_rates, bitbank_output_file_path, indent=4)

        print("Data from bitbank fetched and processed successfully.")



    return send_from_directory('/tmp', 'bitbank.json')

def get_price_from_bylls():
    #Bits is the standard
    from_currency = request.args.get('from_currency', 'BTC')
    to_currency = request.args.get('to_currency', 'Bits')

    if to_currency.lower() == 'bits':
        to_price = 1000000
    elif (to_currency == 'CAD'):
        url = f"https://bylls.com/api/price?from_currency={from_currency}&to_currency={to_currency}"
        try:
            # Send a GET request to the external API
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            input_data = response.json()
            to_price = input_data["public_price"]["to_price"]
        except requests.exceptions.RequestException as e:
          return jsonify({'error': 'An error occurred while fetching data from the external API.'}), 500
    else:
        return jsonify({'error': 'Unsupported currency'}), 500

    data = {
        "public_price": {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "to_price": to_price
            }
        }

    # Add the "mitm" flag with the value "true" at the same level as "public_price"
    data['custom_mitm_rate'] = True

    # Return the modified JSON response
    return jsonify(data)
