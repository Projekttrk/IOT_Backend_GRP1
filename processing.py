from datetime import datetime
import json


def process_request(json_request):
    error_code = json_request['error'].split('https://iib.solutions/')[1]
    plant = json_request['plant']
    version = str(json_request['version'])
    logtime = create_timestamp()
    log_request('test.txt', logtime, plant, version, error_code, '\n')


def log_request(path, *args):
    with open(path, 'a') as f:
        for arg in args:
            f.write(arg)


def create_timestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")


