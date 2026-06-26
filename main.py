import json
import time
import datetime
import fritzconnection.lib.fritzcall as fritzcall
import fritzconnection
import requests

def emergency_detected(pushsafer_api_key, hnr_message_group):
    requests.post("https://www.pushsafer.com/api", data={
        "k": pushsafer_api_key,
        "t": "Hausnotruf wurde ausgelöst!",
        "m": "Ein Hausnotruf wurde erkannt!",
        "d": hnr_message_group,
        "s": "0",
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
isoweekday_test_call = int(config["isoweekdayTestCall"]) #Day of the week, the test call is performed

test_call_time_begin = datetime.datetime.strptime(config["testCallTime"], "%H:%M") #time at wich the test call is performed

test_call_time_begin = datetime.datetime.combine(datetime.date.today(), test_call_time_begin.time())

if time.localtime().tm_isdst == 1:
    test_call_time_begin = test_call_time_begin + datetime.timedelta(hours=1)

if fritzUsr == "":
    connection = fritzconnection.FritzConnection(address = fritzIP, password = fritzPW)
else:
    connection = fritzconnection.FritzConnection(address=fritzIP, password=fritzPW, user=fritzUsr)

fc = fritzcall.FritzCall(fc=connection)

process_calls()

last_call_time = calls[0].Date if calls else None

consecutive_calls = 0

while True:
    test_call_time_begin = datetime.datetime.combine(datetime.date.today(), test_call_time_begin.time())    #current day combined with configured time

    print(len(calls))

    if not( (test_call_time_begin <= datetime.datetime.now() <= (test_call_time_begin + datetime.timedelta(minutes=5))
            and datetime.datetime.now().isoweekday() == isoweekday_test_call) ):
        consecutive_calls = 0

    for call in calls:
        if last_call_time is not None and call.Date <= last_call_time:
            break
        if call.Called == emergency_number:
            if (test_call_time_begin <= datetime.datetime.now() <= (test_call_time_begin + datetime.timedelta(minutes=5))   #wenn innerhalb des Testzeitraums
                    and datetime.datetime.now().isoweekday() == isoweekday_test_call):
                print("skip testing calls")
                consecutive_calls += 1

                if consecutive_calls >= 2:
                    emergency_detected(pushsafer_api_key, hnr_message_group)

            else:
                consecutive_calls = 0
                emergency_detected(pushsafer_api_key, hnr_message_group)

    last_call_time = calls[0].Date if calls else last_call_time
    time.sleep(interval)

    process_calls()