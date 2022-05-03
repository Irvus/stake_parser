from prometheus_client import start_http_server, Summary
import random
import time
import json
import requests

cerberus_link = "https://api.cerberus.zone:1317/staking/validators/cerberusvaloper1xjgspyv73d3k3ewygu0v2gcwwplwxkxg03reqy")
# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    r = requests.get(cerberus_link).json()
    time.sleep(t)


if __name__ == '__main__':
    t = 10
    start_http_server(8000)

    while True:
        process_request(t)
