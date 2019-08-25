import time
import hashlib
import hmac
import requests
import json
from urllib.parse import urlparse


class Bitmex():
    def __init__(self, apiKey, secret):
        self.apiKey = apiKey
        self.secret = secret
        self.apiUrl = 'https://testnet.bitmex.com'

    
    def order(self, symbol, side, orderQty, price, ordType):
        orderData = {
            "symbol": symbol,
            "side": side,
            "orderQty": orderQty,
            "price": price,
            "ordType": ordType
        }
        return self.signed_request('POST', '/api/v1/order', orderData)
        

    def signed_request(self, method, path, data):
        expires = int(round(time.time()) + 5)
        signature = self.generate_signature(method, path, expires, data)
        headers = {
            "Content-Type": "application/json",
            "api-expires": str(expires),
            "api-key": self.apiKey,
            "api-signature": signature
        }
        url = self.apiUrl + path
        return requests.request(method, url, json=data, headers=headers)


    # Generates an API signature.
    # A signature is HMAC_SHA256(secret, verb + path + expires + data), hex encoded.
    # Verb must be uppercased, url is relative, expires must be unix timestamp (in seconds)
    # and the data, if present, must be JSON without whitespace between keys.
    def generate_signature(self, verb, url, expires, data):
        """Generate a request signature compatible with BitMEX."""
        # Parse the url so we can remove the base and extract just the path.
        parsedURL = urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query

        if isinstance(data, (bytes, bytearray)):
            data = data.decode('utf8')

        print("Computing HMAC: %s" % verb + path + str(expires) + str(data))
        message = verb + path + str(expires) + json.dumps(data)

        signature = hmac.new(bytes(self.secret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
        return signature


    