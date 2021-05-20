from pydicom import dcmread
from pydicom.datadict import dictionary_VR
from random import randint
import os
import sys
import csv
import shutil
import logging

src_dicom_path = str(sys.argv[1])

dicom_series_dict = {}

def is_dicom(file):
    file_extension = file.split('.')[-1]
    return file_extension.lower() == 'dcm'

def extract_dicom_header_data(
    dicom_path, mrn, ct_date):
    dicom_img = dcmread(dicom_path)
    series_uid = dicom_img.SeriesInstanceUID

    if series_uid not in dicom_series_dict:
        dicom_series_dict[series_uid] = {}
        dicom_series_dict[series_uid]['patient_name'] = dicom_img.PatientName
        dicom_series_dict[series_uid]['mrn'] = mrn
        dicom_series_dict[series_uid]['study_description'] = dicom_img.StudyDescription
        dicom_series_dict[series_uid]['study_date'] = ct_date
        dicom_series_dict[series_uid]['number_of_slices'] = 0
        dicom_series_dict[series_uid]['slice_thickness'] = dicom_img.SliceThickness
    else:
        dicom_series_dict[series_uid]['number_of_slices'] += 1
    
with open(src_dicom_path + '/dicom_stats.csv', 'w') as output_csv:
    for root, dirs, files in os.walk(src_dicom_path):
        for file in files:
            if is_dicom(file):
                dicom_path = os.path.join(root, file)
                dicom_folder_name = os.path.basename(os.path.dirname(dicom_path))

                mrn = dicom_folder_name.split('_')[0]
                ct_date = dicom_folder_name.split('_')[1]
                extract_dicom_header_data(dicom_path, mrn, ct_date)

    csv_columns = ['patient_name', 'mrn', 'study_description', 'study_date', 'number_of_slices', 'slice_thickness']
    writer = csv.DictWriter(output_csv, fieldnames=csv_columns)
    writer.writeheader()
    for series in dicom_series_dict:
        writer.writerow(dicom_series_dict[series])