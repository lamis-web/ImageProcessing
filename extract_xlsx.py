import sys
import os
import shutil
import pandas as pd

PROJ = 'C19'
INPUT_PATH = sys.argv[1]
EXCEL_PATH = sys.argv[2]

# Create vida case data dictionary from Datasheet
excel_data = pd.read_excel(EXCEL_PATH, usecols='A,AJ,I')
series_dict = {} # { vida_case_id: { proj, subj, img, path } }
num_slices_dict = {} # { accession_number: { case_id, num_slices } }
for _, row in excel_data.iterrows():
    case_id = str(row[0])
    num_slices = row[1]
    accession_number = row[2]

    subj = accession_number.split('_')[0]
    img = accession_number.split('_')[1]
    path = os.path.abspath(INPUT_PATH) + '/' + case_id

    series_dict[case_id] = {
        'Proj': PROJ,
        'Subj': subj,
        'Img': img,
        'ImgDir': path
    }

    # find best cases
    if accession_number not in num_slices_dict:
        num_slices_dict[accession_number] = {
            'case_id': case_id,
            'num_slices': num_slices
        }
    else:
        if num_slices > num_slices_dict[accession_number]['num_slices']:
            case_to_delete = num_slices_dict[accession_number]['case_id']
            num_slices_dict[accession_number]['case_id'] = case_id
            num_slices_dict[accession_number]['num_slices'] = num_slices
            del series_dict[case_to_delete]
        else:
            del series_dict[case_id]

# Find vida cases to process in input directory and change directory name
# case_id(ex: 100) -> subj_img(ex: C19KU100_IN0)
series_to_write = []
indent = ' ' * 4
dirs = [dir for dir in os.listdir(INPUT_PATH) if os.path.isdir(INPUT_PATH + '/' + dir)]
for dir in dirs:
    if dir in series_dict:
        print(dir)
        series_to_write.append(series_dict[dir])
        dest = series_dict[dir]['ImgDir']
        #os.rename(INPUT_PATH +  '/' + dir, dest)

# Write ProjSubList.in
with open(INPUT_PATH + '/' + 'ProjSubjList.in', 'w') as f:
    f.write('Proj' + indent + 'Subj' + indent + 'Img' + indent + 'Imgdir' + '\n')
    for series in series_to_write:
        f.write(series['Proj'] + indent + series['Subj'] + indent + series['Img'] + indent + series['ImgDir'] + '\n')

