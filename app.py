from flask import Flask, request, jsonify
import requests

from price_api import get_price_from_bylls, get_price_from_bitbank, get_price_from_coingecko

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "This is a MITM server emulating https://api.coingecko.com/api/v3/exchange_rates/, https://bylls.com/api/price?from_currency=BTC&to_currency=CAD and https://public.bitbank.cc/tickers "

@app.route('/api/price', methods=['GET'])
def from_bylls():
    return get_price_from_bylls()

#https://api.coingecko.com/api/v3/exchange_rates/
@app.route('/api/v3/exchange_rates')
def from_coingecko():
    return get_price_from_coingecko()

@app.route('/tickers')
def return_bitbank():
    return get_price_from_bitbank()

if __name__ == '__main__':


    certfile = '/certificates/customrates.local.MITM.crt'
    keyfile = '/certificates/MITM.key'
    app.run(ssl_context=(certfile, keyfile), host='192.168.99.3', port=443, debug=True)
