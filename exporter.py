import json
import requests
import time

from prometheus_client import start_http_server, Info
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

i = Info('coingecko_metric', 'Mintscan info', ['chain'])
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}

validators = [
    {'name': 'cerberus-2',
     'url': "https://api.cerberus.zone:1317/staking/validators/cerberusvaloper1xjgspyv73d3k3ewygu0v2gcwwplwxkxg03reqy"
     },
    {'name': 'ki',
     'url': "https://api-mainnet.blockchain.ki/staking/validators/kivaloper19seaxuh9wp3zum42w6flrjsr5raptxhy3l8qvw"
     },
    {'name': 'ixo',
     'url': "https://impacthub.ixo.world/rest/staking/validators/ixovaloper12g6xke0lu758u8dtan8efsdhe2xxwxwh4lrjax"
     },
    {'name': 'desmos',
     'url': "https://api-desmos.cosmostation.io/v1/staking/validator/desmosvaloper1zngdx77g9ywnwmwpwvj9w2eqcs6fhw78gn02d8"
     },
    {'name': 'injective-protocol',
     'url': "https://api-inj.cosmostation.io/v1/staking/validator/injvaloper1kpfxtqt5cmlew46dem32fqlk5g6k4wyueh4szu"
     },
    {'name': 'stargaze',
     'url': "https://api-stargaze.cosmostation.io/v1/staking/validator/starsvaloper15cu52e36jth9gqr0muq755syvgyr96cr98a549"
     }
]


def process_request(link, net_name):
    parsed_json = requests.get(link).json()
    coin_cost = float(cg.get_price(ids=net_name, vs_currencies='usd').get(net_name).get('usd'))

    try:
        temp = str(float(parsed_json.get('result').get('tokens')) / 1000000)
    except:
        if (parsed_json.get('jailed') == True):
            temp = str(float(parsed_json.get('tokens')) / 10e17)
        else:
            temp = str(float(parsed_json.get('tokens')) / 1000000)

    bounded_tokens = {'net_name': net_name, 'staked tokens': temp,
                      'turnover': str(float(temp) * coin_cost)}

    return bounded_tokens


def job():
    for validator in validators:
        try:
            bound_tokens = process_request(validator['url'], validator['name'])
            print(bound_tokens)

            i.labels(chain=validator['name']).info({
                f"staked tokens": bound_tokens['staked tokens'],
                f"turnover": bound_tokens['turnover'],
            })
        except Exception:
            i.labels(chain=validator['name']).info({
                f"staked_tokens": "-1",
                f"turnover": "-1"
            })


if __name__ == '__main__':
    t = 3600
    start_http_server(9879)

    while True:
        job()
        time.sleep(t)
