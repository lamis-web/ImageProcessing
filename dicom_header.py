import os
from pydicom import dcmread
from pydicom import Dataset
import sys


def is_dicom(file):
    file_extension = file.split('.')[-1]
    return file_extension == 'dcm'

    
# MAIN
if __name__ == '__main__':
    directory = sys.argv[1]
    print("===================================================")

    patient_id       = input('PATIENT ID/NAME  : ')
    accession_number = input('ACCESSION NUMBER : ')


    for root, dirs, files in os.walk(directory):
        for file in files:
            if (is_dicom(file)):
                ds = dcmread(os.path.join(root, file))  
                ds['PatientID'].value = patient_id
                ds['PatientName'].value = patient_id
                ds['AccessionNumber'].value = accession_number
                print(os.path.join(root, file) + ' ==> Overwriting ... ')
            else:
                print(os.path.join(root, file) + ' ==> Non dicom ... ')

    