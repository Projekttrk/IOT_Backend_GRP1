from datetime import datetime
import pandas as pd
import configparser


def process_request(json_request):
    config = configparser.ConfigParser()
    config.read('application/error_conf.ini')
    codenummer = json_request['error'].split(' ')[1]
    codefarbe = json_request['error'].split(' ')[3]
    logtime = create_timestamp()
    date = logtime.split(' ')[0]
    time = logtime.split(' ')[1]
    log_request('test.txt', logtime, codenummer, codefarbe, '\n')

    error_code = config['errorcodes'][codenummer]
    prefix = config['Prefix'][codenummer]
    codetype = config['codetype'][codenummer]
    location = config['location'][codenummer]
    faultcode = config['faultcode'][codenummer]
    export = [[prefix],[codetype],[location],[faultcode],["Error"],[error_code],[date],[time],['new']]
    df = pd.read_excel("export_dataframe.xlsx", encoding= "CP1252")
    df2 = pd.DataFrame.from_dict(export)
    df = df.append(df2)
    print(df)

    df.to_excel(r"export_dataframe.xlsx", index=False, header=True)


def log_request(path, *args):
    with open(path, 'a') as f:
        for arg in args:
            f.write(str(arg))


def create_timestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%d.%b.%Y (%H:%M:%S)")


