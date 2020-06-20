from datetime import datetime
import pandas as pd


def process_request(json_request):
    codenummer = int(json_request['error'].split(' ')[1])
    codefarbe = json_request['error'].split(' ')[3]
    logtime = create_timestamp()
    log_request('test.txt', logtime, codenummer, codefarbe, '\n')

    export = {'Error_code': [codenummer],'Codefarbe': [codefarbe], 'Timestamp': [logtime]}
    df = pd.read_excel("export_dataframe.xlsx", encoding= "CP1252")
    df2 = pd.DataFrame.from_dict(export)
    df = df.append(df2)
    print(df)

    df.to_excel(r"export_dataframe.xlsx", index=False, header=True)


def log_request(path, *args):
    with open(path, 'a') as f:
        for arg in args:
            f.write(arg)


def create_timestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")


