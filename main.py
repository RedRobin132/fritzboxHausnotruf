import fritzconnection.lib.fritzcall as fritzcall
import fritzconnection
import requests

pushsafer_api_key = "PXPCwje8FymJn6CVTCwl"

connection = fritzconnection.FritzConnection("192.168.177.1", password= "inside5630")

fc = fritzcall.FritzCall(fc=connection)

calls = fc.get_calls()
print(len(calls))
'''
for call in calls:
    print(call)
'''