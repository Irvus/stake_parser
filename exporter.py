import json
import requests
import time

from prometheus_client import start_http_server, Info
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

cerberus_link = "https://api.cerberus.zone:1317/staking/validators" \
                "/cerberusvaloper1xjgspyv73d3k3ewygu0v2gcwwplwxkxg03reqy"

bounded_tokens = Info('my_inprogress_requests', 'here was Ilia')


def process_request(t):
    parsed_json = requests.get(cerberus_link).json()
    coin_cost = float(cg.get_price(ids='cerberus-2', vs_currencies='usd').get('cerberus-2').get('usd'))
    bounded_tokens.info({'staked tokens': parsed_json.get('result').get('tokens'),
                         'turnover': str(float(parsed_json.get('result').get('tokens')) * coin_cost)})
    time.sleep(t)


if __name__ == '__main__':
    t = 10
    start_http_server(8000)

    while True:
        process_request(t)
