from pydicom import dcmread
from pydicom.datadict import dictionary_VR
from random import randint
from tqdm import tqdm
import argparse
import os
import csv
import shutil
import copy
import logging

# Create an argumnet parser
parser = argparse.ArgumentParser(
    description='Recursively extract DICOM metadata of the source folder')
parser.add_argument('src', metavar='src', type=str, help='DICOM source folder')
parser.add_argument('dst', metavar='dst', type=str, help='DICOM source folder')
args = parser.parse_args()

# Create a logger
logging.basicConfig(filename='dicom_deidentifier.log', level=logging.WARNING,
                    filemode='a', format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

src_dicom_path = args.src
dst_dicom_path = args.dst

dicom_series = {}  # { SeriesInstanceUID : { Series Data } }
dicom_series_paths = {}  # { SeriesInstanceUID : { Img Paths } }


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
            dicom_series[series_uid]['patient_name'] = dicom_img.PatientName
        except:
            dicom_series[series_uid]['patient_name'] = ''
        try:
            dicom_series[series_uid]['patient_id'] = dicom_img.PatientID
        except:
            dicom_series[series_uid]['patinet_id'] = ''
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
        dicom_series[series_uid]['mrn'] = mrn
        dicom_series[series_uid]['study_date'] = ct_date
        dicom_series[series_uid]['number_of_slices'] = 1
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
    csv_columns = ['mrn', 'study_date', 'patient_name', 'patient_id',
                   'slice_thickness', 'number_of_slices', 'study_description', 'series_description']
    writer = csv.DictWriter(output_csv, fieldnames=csv_columns)
    writer.writeheader()
    for series_uid in dicom_series:
        writer.writerow(dicom_series[series_uid])
print('----- Done')

# pick series of interest
dicom_series_selected = copy.deepcopy(dicom_series)
abandoned_keywords = ['SCOUT', 'COR', 'SAG', 'MIP']

print('>>> Selecting series of interest', end=' ')
for series_uid in dicom_series:
    series_meta = dicom_series[series_uid]
    if series_meta['slice_thickness'] == '' or int(series_meta['slice_thickness']) > 5:
        dicom_series_selected.pop(series_uid)
        dicom_series_paths.pop(series_uid)
        continue
    if int(series_meta['number_of_slices']) < 10:
        dicom_series_selected.pop(series_uid)
        dicom_series_paths.pop(series_uid)
        continue
    for keyword in abandoned_keywords:
        if keyword in series_meta['series_description'].upper():
            dicom_series_selected.pop(series_uid)
            dicom_series_paths.pop(series_uid)
            continue
print('----- Done')

# write to csv
print('>>> Writing selected metadata to dicom_metadata_selected.csv', end=' ')
with open(dst_dicom_path + '/dicom_metadata_selected.csv', 'w', newline='') as output_csv:
    csv_columns = ['mrn', 'study_date', 'patient_name', 'patient_id',
                   'slice_thickness', 'number_of_slices', 'study_description', 'series_description']
    writer = csv.DictWriter(output_csv, fieldnames=csv_columns)
    writer.writeheader()
    for series_uid in dicom_series_selected:
        writer.writerow(dicom_series_selected[series_uid])
print('----- Done')

# Copy selected DICOM series to destination
print('>>> Coping selected series to the destination')
for series_uid in tqdm(dicom_series_selected):
    series_meta = dicom_series_selected[series_uid]

    dicom_source_paths = dicom_series_paths[series_uid]
    dicom_source_folder_name = os.path.basename(
        os.path.dirname(dicom_source_paths[0]))

    dicom_destination_folder_path = dst_dicom_path + '/' + dicom_source_folder_name
    if not os.path.exists(dicom_destination_folder_path):
        os.makedirs(dicom_destination_folder_path)

    dicom_destination_series_path = dicom_destination_folder_path + \
        '/' + series_meta['series_description']
    if not os.path.exists(dicom_destination_series_path):
        os.makedirs(dicom_destination_series_path)

    for dicom_source_slice_path in dicom_source_paths:
        dicom_source_slice_filename = os.path.basename(dicom_source_slice_path)
        dicom_destination_slice_path = dicom_destination_series_path + \
            '/' + dicom_source_slice_filename
        shutil.copyfile(dicom_source_slice_path, dicom_destination_slice_path)
