from os import lseek
import pandas as pd

START_VIDA_CASE_ID = 960
EXCEL_PATH = './Data/Datasheet/DataSheet_20210629.xlsx'
df = pd.read_excel(EXCEL_PATH, sheet_name=0)
df = df[df['VidaCaseID'] >= START_VIDA_CASE_ID]

SUCCESS_COUNT = 0
NEED_LABELS_COUNT = 0
FAILURE_COUNT = 0

for _, row in df.iterrows():
    if row['Vida Progress'] == 'Success':
        SUCCESS_COUNT += 1
    elif row['Vida Progress'] == 'Needs Labels':
        NEED_LABELS_COUNT += 1
    else:
        FAILURE_COUNT += 1

print(
    f'SUCCESS: {SUCCESS_COUNT}, NEED_LABELS: {NEED_LABELS_COUNT}, FAILURE: {FAILURE_COUNT}')

need_to_work_df = df[(df['Vida Progress'] == 'Success')
                     & (df['Progress'] != 'Done')]
print(need_to_work_df['SliceThickness_mm'].value_counts())
