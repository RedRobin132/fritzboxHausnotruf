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
        "d": hnr_message_group,
        "s": "2",
        "v": "2",
        "i": "74",
        "l": "60",
        "ut": "Website",
        "pr": 2
    })

def fritz_request_error(e):
    requests.post("https://www.pushsafer.com/api", data={
        "k": pushsafer_api_key,
        "t": "Request Error occured!",
        "m": f"There was an error fetching call data.: {e}",
        "d": developer_message_group,
        "s": "2",
        "v": "2",
        "i": "74",
        "l": "60",
        "ut": "Website",
        "pr": 0
    })

def process_calls():
    global calls, interval, error_status, e
    try:
        calls = fc.get_calls(days=1)
        interval = 10
        error_status = False
    except Exception as e:
        if not error_status:
            fritz_request_error(e)

        calls = []
        print(e)
        interval = 60
        error_status = True


with open('config.json') as config_file:
    config = json.load(config_file)

error_status = False

pushsafer_api_key = config["pushsaferApiKey"]
fritzIP = config["fritzIP"]
fritzPW = config["fritzPW"]
fritzUsr = config["fritzUsr"]
emergency_number = config["emergencyNumber"]
developer_message_group = config["DeveloperMSG"]
hnr_message_group = config["HNRGroup"]

if fritzUsr == "":
    connection = fritzconnection.FritzConnection(address = fritzIP, password = fritzPW)
else:
    connection = fritzconnection.FritzConnection(address=fritzIP, password=fritzPW, user=fritzUsr)

fc = fritzcall.FritzCall(fc=connection)

process_calls()

last_number_of_calls = len(calls)


while True:
    current_number_of_calls = len(calls)
    print(current_number_of_calls)

    for i in range(current_number_of_calls-last_number_of_calls):
        if calls[i].Called == emergency_number:
            emergency_detected(pushsafer_api_key)

    last_number_of_calls = current_number_of_calls
    time.sleep(interval)

    process_calls()
