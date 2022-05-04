from prometheus_client import start_http_server, Gauge, Summary
import random
import time
import json
import requests
from pycoingecko import CoinGeckoAPI


cg = CoinGeckoAPI()

cerberus_link = "https://api.cerberus.zone:1317/staking/validators/cerberusvaloper1xjgspyv73d3k3ewygu0v2gcwwplwxkxg03reqy"
# Create a metric to track time spent and requests made.
bounded_tokens = Gauge('my_inprogress_requests', 'Description of gauge')


# Decorate function with metric.
@bounded_tokens.track_inprogress()
def process_request(t):
    parsed_json = requests.get(cerberus_link).json()
    coin_cost = float(k.get('cerberus-2').get('usd'))
    bounded_tokens.set_function(lambda: int(parsed_json.get('result').get('tokens')))
    time.sleep(t)


if __name__ == '__main__':
    t = 10
    start_http_server(8000)

    while True:
        process_request(t)
