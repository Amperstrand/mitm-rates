# price_api.py

from flask import jsonify, request
import requests

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
