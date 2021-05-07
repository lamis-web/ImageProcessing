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

    if len(sys.argv) > 2:
        print("===================================================")

        ds = dcmread(directory)  # 만약 두번째 argument에 무언가가 있다면, 정보만 보여준다.
        print(ds)        

    else:
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
                    ds.save_as(os.path.join(root, file))
                    print(os.path.join(root, file) + ' ==> Overwriting ... ')
                else:
                    print(os.path.join(root, file) + ' ==> Non dicom ... ')

    