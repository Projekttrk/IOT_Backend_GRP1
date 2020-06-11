from datetime import datetime
import pandas as pd

def process_request(json_request):
    error_code = json_request['error'].split('https://iib.solutions/')[1]
    plant = json_request['plant']
    version = str(json_request['version'])
    logtime = create_timestamp()
    log_request('test.txt', logtime, plant, version, error_code, '\n')

    export = {'Error_code': [error_code],'Plant': [Plant], 'Version': [version], 'Timestamp': [logtime]}
    df = pd.DataFrame(export, columns=['Error_code', 'Plant','Version','Timestamp'])
    df.to_excel(r"C:\Users\Jovan\Desktop\export_dataframe.xlsx", index=False, header=True)


def log_request(path, *args):
    with open(path, 'a') as f:
        for arg in args:
            f.write(arg)


def create_timestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")


