# Usage
# - python prepare_ProjSubjList.py

from datetime import datetime
import tarfile
from pathlib import Path
import pandas as pd
from tqdm import tqdm
# from dotenv import dotenv_values
# import paramiko
# from scp import SCPClient


PROJ = 'C19'
CASE_ID_LIST = [960]
OUTPUT_FOLDER_NAME = f'VIDA_20210701-01_{PROJ}_TK'
PATH_IN_B2 = f'/data4/common/{PROJ}'
OUTPUT_PATH = 'Data_to_send'
DATASHEET_PATH = 'Data/Datasheet/DataSheet.xlsx'
VIDA_VISION_PATH = 'E:/VIDA/VIDAvision2.2'


print('>>> Construct Dataframe for ProjSubjList.in from Datasheet.xlsx', end=' ')
datasheet_df = pd.read_excel(DATASHEET_PATH, usecols='A:C,I')
case_data_list = []
for case in CASE_ID_LIST:
    try:
        row = datasheet_df.loc[datasheet_df['VidaCaseID'] == case]
        temp_dict = {}
        for k1, v1 in row.to_dict().items():
            for k2, v2 in v1.items():
                temp_dict[k1] = v2
        temp_dict['ImgDir'] = f'{PATH_IN_B2}/{OUTPUT_FOLDER_NAME}/{case}'
        case_data_list.append(temp_dict)
    except:
        print(f'Cannot find case id {case}')
case_data_df = pd.DataFrame(case_data_list)
case_data_df.rename(columns={'IN/EX': 'Img'}, inplace=True)
case_data_df.drop(columns=['VidaCaseID'], inplace=True)
print('----- Done')


print('>>> Create ProjSubjList.in', end=' ')
today = datetime.today().strftime('%Y%m%d')
projSubjListTitle = f'ProjSubjList.in.{today}_{PROJ}'
case_data_df = case_data_df.to_csv(
    index=False, line_terminator='\n').replace(',', '    ')
with open(f'{OUTPUT_PATH}/{projSubjListTitle}', 'w') as f:
    f.write(case_data_df)
print('----- Done')


print('>>>  Compress VIDA results into one tar file')
with tarfile.open(f'{OUTPUT_PATH}/{OUTPUT_FOLDER_NAME}.tar.bz2', 'w:bz2') as tar:
    for case in tqdm(CASE_ID_LIST):
        tar.add(Path(f'{VIDA_VISION_PATH}/{case}'), f'{OUTPUT_FOLDER_NAME}/{case}')


# print('>>>  Send Data to B2')
# class FastTransport(paramiko.Transport):
#     def __init__(self, sock):
#         super(FastTransport, self).__init__(sock)
#         self.window_size = 2147483647
#         self.packetizer.REKEY_BYTES = pow(2, 40)
#         self.packetizer.REKEY_PACKETS = pow(2, 40)

# ssh_config = dotenv_values('.env')
# ssh_conn = FastTransport((ssh_config['SSH_HOST'], int(ssh_config['SSH_PORT'])))
# ssh_conn.connect(username=ssh_config['SSH_USERNAME'], password=ssh_config['SSH_PW'])
# sftp = paramiko.SFTPClient.from_transport(ssh_conn)
# sftp.put(Path(f'{OUTPUT_PATH}/{projSubjListTitle}'), f'{PATH_IN_B2}/{projSubjListTitle}')
# sftp.put(f'{OUTPUT_PATH}/{OUTPUT_FOLDER_NAME}.tar.bz2', f'{PATH_IN_B2}/{OUTPUT_FOLDER_NAME}.tar.bz2')
# sftp.close()

# ssh = SSHClient()
# ssh.load_system_host_keys()
# ssh.connect(ssh_config['SSH_HOST'], port=ssh_config['SSH_PORT'], username=ssh_config['SSH_USERNAME'], password=ssh_config['SSH_PW'], look_for_keys=False)

# def progress(filename, size, sent):
#     sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

# with SCPClient(ssh.get_transport(), progress=progress) as scp:
#     scp.put(f'{OUTPUT_PATH}/{projSubjListTitle}', remote_path=PATH_IN_B2)
#     scp.put(f'{OUTPUT_PATH}/{OUTPUT_FOLDER_NAME}.tar.bz2', remote_path=PATH_IN_B2)