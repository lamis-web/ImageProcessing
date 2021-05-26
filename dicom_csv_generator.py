from pydicom import dcmread
from pydicom.datadict import dictionary_VR
from random import randint
from tqdm import tqdm
import argparse
import os
import sys
import csv
import shutil
import logging

parser = argparse.ArgumentParser(description='Recursively extract DICOM metadata of the source folder')
parser.add_argument('src', metavar='src', type=str, help='DICOM source folder')
args = parser.parse_args()

src_dicom_path = args.src
dicom_series = {} # { SeriesInstanceUID : { Series Data } }
dicom_series_of_interest = {} # { Dicom Folder Name : Dicom Path With Min Slice Thickness }

def extract_dicom_header(
        dicom_path, mrn, ct_date):
    dicom_img = dcmread(dicom_path)
    try:
        series_uid = dicom_img.SeriesInstanceUID
    except:
        print("No SeriesInstanceUID")
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
    else:
        dicom_series[series_uid]['number_of_slices'] += 1

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
for dicom_slice_path in tqdm(walkdir(src_dicom_path), total=file_count):
    if not dicom_slice_path.endswith('.dcm'):
        continue
    series_name = os.path.basename(os.path.dirname(dicom_slice_path))
    mrn = series_name.split('_')[0]
    ct_date = series_name.split('_')[1]
    extract_dicom_header(dicom_slice_path, mrn, ct_date)

# write to csv
with open(src_dicom_path + '/dicom_stats.csv', 'w', newline='') as output_csv:
    csv_columns = ['mrn', 'study_date', 'patient_name', 'patient_id',
                    'slice_thickness', 'number_of_slices', 'study_description', 'series_description']
    writer = csv.DictWriter(output_csv, fieldnames=csv_columns)
    writer.writeheader()
    for series in dicom_series:
        writer.writerow(dicom_series[series])
