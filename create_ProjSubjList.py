import tarfile
from pathlib import Path
import pandas as pd
from tqdm import tqdm

CASE_ID_LIST = [960, 968, 962, 964, 991, 990, 1001, 1002, 1006, 1005]
DATASHEET_PATH = 'Data/Datasheet/DataSheet.xlsx'
VIDA_VISION_PATH = 'E:/VIDA/VIDAvision2.2'
PATH_IN_B2 = '/data4/common/C19'
OUTPUT_TAR_FILE_PATH = 'Data_to_send/VIDA_20210623-23_C19_TK.tar.bz2'

# Construct Dataframe for ProjSubjList.in from Datasheet.xlsx
datasheet_df = pd.read_excel(DATASHEET_PATH, usecols='A:C,I')
case_data_list = []
case_data_df = ''
for case in CASE_ID_LIST:
    try:
        row = datasheet_df.loc[datasheet_df['VidaCaseID'] == case]
        temp_dict = {}
        for k1, v1 in row.to_dict().items():
            for k2, v2 in v1.items():
                temp_dict[k1] = v2
        temp_dict['ImgDir'] = f'{PATH_IN_B2}/VIDA/VIDAvision2.2/{case}'
        case_data_list.append(temp_dict)
        case_data_df = pd.DataFrame(case_data_list)
        case_data_df.rename(columns={'IN/EX': 'Img'}, inplace=True)
        case_data_df.drop(columns=['VidaCaseID'], inplace=True)
    except:
        print(f'Cannot find case id {case}')

# Create ProjSubjList.in
case_data_df = case_data_df.to_csv(
    index=False, line_terminator='\n').replace(',', '    ')
with open('Data_to_send/ProjSubjList.in', 'w') as f:
    f.write(case_data_df)

# Compress VIDA cases into one tar file
with tarfile.open(OUTPUT_TAR_FILE_PATH, 'w:bz2') as tar:
    for case in tqdm(CASE_ID_LIST):
        tar.add(Path(f'{VIDA_VISION_PATH}/{case}'))

# Send data to B2
