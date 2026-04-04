import json
import time
import datetime
import fritzconnection.lib.fritzcall as fritzcall
import fritzconnection
import requests

with open('config.json') as config_file:
    config = json.load(config_file)


pushsafer_api_key = config["pushsaferApiKey"]
fritzIP = config["fritzIP"]
fritzPW = config["fritzPW"]

connection = fritzconnection.FritzConnection(address = fritzIP, password = fritzPW)

fc = fritzcall.FritzCall(fc=connection)
calls = fc.get_calls(days=1)
last_number_of_calls = len(calls)


interval = 10
while True:

    calls = fc.get_calls(days=1)
    current_number_of_calls = len(calls)
    print(current_number_of_calls)

    for i in range(current_number_of_calls-last_number_of_calls):
        print(calls[i])

    last_number_of_calls = current_number_of_calls
    time.sleep(interval)