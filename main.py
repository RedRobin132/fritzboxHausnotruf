import json

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

calls = fc.get_calls()
print(len(calls))
'''
for call in calls:
    print(call)
'''