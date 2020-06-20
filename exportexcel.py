import pandas as pd
from openpyxl import load_workbook
# new dataframe with same columns
df = pd.DataFrame({'Name': ['E','F','G','H'],
                   'Age': [100,70,40,60]})
writer = pd.ExcelWriter(r"C:\Users\Jovan\Desktop\export_dataframe.xlsx", engine='openpyxl')
# try to open an existing workbook
writer.book = load_workbook(r"C:\Users\Jovan\Desktop\export_dataframe.xlsx")
# copy existing sheets
writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
# read existing file
reader = pd.read_excel(r"C:\Users\Jovan\Desktop\export_dataframe.xlsx")
# write out the new sheet
df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)

writer.close()