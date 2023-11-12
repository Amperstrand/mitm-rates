# price_api.py

from flask import jsonify, request
import requests

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
