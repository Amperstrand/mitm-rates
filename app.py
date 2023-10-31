from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "This is a MITM server emulating https://api.coingecko.com/api/v3/exchange_rates/"

@app.route('/api/v3/exchange_rates')
def exchange_rates():
    return send_from_directory('/tmp', 'exchange_rates_10x.json')

if __name__ == '__main__':
    certfile = '/certificates/api.coingecko.com.MITM.crt'
    keyfile = '/certificates/api.coingecko.com.MITM.key'
    app.run(ssl_context=(certfile, keyfile), host='192.168.99.3', port=443, debug=True)
