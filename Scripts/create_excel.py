# import pandas as pd

# # dataframe Name and Age columns
# df = pd.DataFrame({'Col1': ['A', 'B', 'C', 'D'],
#                    'Col2': [10, 0, 30, 50]})

# # Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter('sample.xlsx', engine='xlsxwriter')

# # Convert the dataframe to an XlsxWriter Excel object.
# df.to_excel(writer, sheet_name='Sheet1', index=False)

# # Close the Pandas Excel writer and output the Excel file.
# writer.save()

import pandas as pd
from openpyxl import load_workbook
# new dataframe with same columns
df = pd.DataFrame({'Col1': ['E','F','G','H'],
                   'Col2': [100,70,40,60]})
writer = pd.ExcelWriter('sample.xlsx', engine='openpyxl')
# try to open an existing workbook
writer.book = load_workbook('sample.xlsx')
# copy existing sheets
writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
# read existing file
reader = pd.read_excel(r'sample.xlsx')
# write out the new sheet
df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)

writer.close()