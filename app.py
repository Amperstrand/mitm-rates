from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import json

from price_api import get_price

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "This is a MITM server emulating https://api.coingecko.com/api/v3/exchange_rates/, https://bylls.com/api/price?from_currency=BTC&to_currency=CAD and https://public.bitbank.cc/tickers "

app.add_url_rule('/api/price', 'get_price', get_price, methods=['GET'])

#https://api.coingecko.com/api/v3/exchange_rates/
@app.route('/api/v3/exchange_rates')
def return_coingecko_10x():
    return send_from_directory('/tmp', 'exchange_rates_10x.json')

@app.route('/tickers')
def return_bitbank():
    return send_from_directory('/tmp', 'bitbank.json')

if __name__ == '__main__':

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


    certfile = '/certificates/customrates.local.MITM.crt'
    keyfile = '/certificates/MITM.key'
    app.run(ssl_context=(certfile, keyfile), host='192.168.99.3', port=443, debug=True)
