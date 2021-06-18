from pydicom import dcmread
from pydicom.datadict import dictionary_VR
from random import randint
from tqdm import tqdm
import pandas as pd
import argparse
import os
import csv
import logging

# Create an argumnet parser
parser = argparse.ArgumentParser(
    description='Recursively de-identify and copy DICOM images from src to dst')
parser.add_argument('src', metavar='src', type=str,
                    help='DICOM source folder path')
parser.add_argument('dst', metavar='dst', type=str,
                    help='DICOM destination folder path')
parser.add_argument('xls', metavar='xls', type=str,
                    help='Excel metadata sheet path')
args = parser.parse_args()

# Create a logger
logging.basicConfig(filename='metadata_log', level=logging.WARNING,
                    filemode='w', format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

src_dicom_path = args.src
dst_dicom_path = args.dst
excel_path = args.xls

dicom_series = {}  # {SeriesInstanceUID : {Series Data}}
dicom_series_paths = {}  # {SeriesInstanceUID : [Img Paths]}
series_id_dict = {}  # {'Series_UID' : ['Subj_ID', 'Img_ID']}


def extract_dicom_header(
        dicom_path, mrn, ct_date):
    dicom_img = dcmread(dicom_path)
    try:
        series_uid = dicom_img.SeriesInstanceUID
    except:
        logger.error(f'{dicom_path} - No SeriesInstanceUID')
        return

    if series_uid not in dicom_series:
        dicom_series[series_uid] = {}
        try:
            dicom_series[series_uid]['study_description'] = dicom_img.StudyDescription
        except:
            dicom_series[series_uid]['study_description'] = ''
        try:
            dicom_series[series_uid]['series_description'] = dicom_img.SeriesDescription
        except:
            dicom_series[series_uid]['series_description'] = ''
        if dicom_img.get('SliceThickness'):
            dicom_series[series_uid]['slice_thickness'] = dicom_img.SliceThickness
        else:
            dicom_series[series_uid]['slice_thickness'] = ''
        dicom_folder_name = os.path.basename(os.path.dirname(dicom_path))
        if dicom_folder_name in series_id_dict:
            dicom_series[series_uid]['subj'] = series_id_dict[dicom_folder_name][0]
            dicom_series[series_uid]['img'] = series_id_dict[dicom_folder_name][1]
        else:
            logger.warn(
                f'cant find excel data for folder name {dicom_folder_name}')
        dicom_series[series_uid]['number_of_slices'] = 1
        dicom_series[series_uid]['mrn'] = mrn
        dicom_series[series_uid]['study_date'] = ct_date
        dicom_series[series_uid]['path'] = os.path.dirname(dicom_path)
        dicom_series_paths[series_uid] = [dicom_path]
    else:
        dicom_series[series_uid]['number_of_slices'] += 1
        dicom_series_paths[series_uid].append(dicom_path)


# precounting files
file_count = 0
for root, dirs, files in os.walk(src_dicom_path):
    for file in files:
        file_count += 1


def walkdir(src):
    for base, dirs, files in os.walk(src):
        for file in files:
            yield os.path.join(base, file)


# Construct series_id_dict from Excel metadata sheet
print('>>> Construct subjID & imgID from excel metadata sheet', end='')
excel_data = pd.read_excel(excel_path, header=8, usecols='A,C,I,J')
for _, row in excel_data.iterrows():
    subj_id = row['Subj']
    mrn = str(row['mrn']).zfill(7)
    ctdate = row['date'].strftime('%Y%m%d') if type(
        row['date']) == pd.Timestamp else ''
    if ctdate == '':
        logger.warning(f'{subj_id} cannot get ctdate from {excel_path}')
    key = mrn + '_' + ctdate + '_all'
    img_id = str(row['Time'])

    series_id_dict[key] = [subj_id, img_id]
print('----- Done')

# recursively read dicom images
print('>>> Generating metadata dictionary')
for dicom_slice_path in tqdm(walkdir(src_dicom_path), total=file_count):
    if not dicom_slice_path.endswith('.dcm'):
        continue
    series_name = os.path.basename(os.path.dirname(dicom_slice_path))
    mrn = series_name.split('_')[0]
    ct_date = series_name.split('_')[1]
    extract_dicom_header(dicom_slice_path, mrn, ct_date)

# write to csv
print('>>> Writing all metadata to dicom_metadata_all.csv', end=' ')
with open(dst_dicom_path + '/dicom_metadata_all.csv', 'w', newline='') as output_csv:
    csv_columns = ['subj', 'img', 'mrn', 'study_date', 'slice_thickness',
                   'number_of_slices', 'study_description', 'series_description', 'path']
    writer = csv.DictWriter(output_csv, fieldnames=csv_columns)
    writer.writeheader()
    for series_uid in dicom_series:
        writer.writerow(dicom_series[series_uid])
print('----- Done')

# pick series of interest
abandoned_keywords = ['SCOUT', 'COR', 'SAG', 'MIP', 'AX', 'EXP']
print('>>> Selecting series of interest', end=' ')
for series_uid in list(dicom_series):
    series_meta = dicom_series[series_uid]
    if series_meta['slice_thickness'] == '' or int(series_meta['slice_thickness']) >= 5:
        del dicom_series[series_uid]
        del dicom_series_paths[series_uid]
        continue
    if int(series_meta['number_of_slices']) < 10:
        del dicom_series[series_uid]
        del dicom_series_paths[series_uid]
        continue
    for keyword in abandoned_keywords:
        if keyword in series_meta['series_description'].upper():
            del dicom_series[series_uid]
            del dicom_series_paths[series_uid]
            break
print('----- Done')

# write to csv
print('>>> Writing selected metadata to dicom_metadata_selected.csv', end=' ')
with open(dst_dicom_path + '/dicom_metadata_selected.csv', 'w', newline='') as output_csv:
    csv_columns = ['subj', 'img', 'mrn', 'study_date', 'slice_thickness',
                   'number_of_slices', 'study_description', 'series_description', 'path']
    writer = csv.DictWriter(output_csv, fieldnames=csv_columns)
    writer.writeheader()
    for series_uid in dicom_series:
        writer.writerow(dicom_series[series_uid])
print('----- Done')
