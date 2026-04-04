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


interval = 10
while True:

    calls = fc.get_calls(days=1)
    print(len(calls))

    for call in calls:

        if datetime.datetime.now() - call.date <= datetime.timedelta(seconds=interval+5):
            print(call)
        else:
            break


    time.sleep(interval)