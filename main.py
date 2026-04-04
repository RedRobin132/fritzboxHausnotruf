import json
import time
import datetime
import fritzconnection.lib.fritzcall as fritzcall
import fritzconnection
import requests

def emergency_detected(pushsafer_api_key):
    requests.post("https://www.pushsafer.com/api", data={
        "k": pushsafer_api_key,
        "t": "Hausnotruf wurde ausgelöst!",
        "m": "Ein Hausnotruf wurde erkannt!",
        "d": "a",
        "s": "2",
        "v": "2",
        "i": "74",
        "l": "60",
        "ut": "Website",
        "pr": 2
    })

with open('config.json') as config_file:
    config = json.load(config_file)


pushsafer_api_key = config["pushsaferApiKey"]
fritzIP = config["fritzIP"]
fritzPW = config["fritzPW"]
emergency_number = config["emergencyNumber"]

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
        if calls[i].Called == emergency_number:
            emergency_detected(pushsafer_api_key)

    last_number_of_calls = current_number_of_calls
    time.sleep(interval)