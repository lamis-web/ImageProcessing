# Dicom Manager

import os
import sys
import httplib2
import base64
import uuid
import requests
import argparse
from progress.bar import IncrementalBar
from typing import Dict
from pydicom import dcmread
import glob



HOST_URL = '127.0.0.1'
ORTHANC_PORT = 8042
ORTHANC_URL = 'http://%s:%d/instances' % (HOST_URL, ORTHANC_PORT)
PULMORAD_ROOT_UID = '1.2.826.0.1.3680043.8.499.'

# Exception
class FilePathException(Exception):
    '''
    Exception raised when the file does not start in ImageData_KSTR
    '''
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return f' -> Folder Path has to be in ImageData_KSTR, not {self.root}'


def is_dicom(file):
    file_extension = file.split('.')[-1]
    return file_extension == 'dcm' or file_extension == 'DCM'

def isDirExist(directory):
    for i in os.listdir(directory):
        if os.path.isdir(f'{directory}/{i}'):
            return True
    return False

class App:
    def __init__(self, args):
        self.args = args
        self.dir = args.dicom_directory[0]
        self.storage = {}
        self.success_count = 0
        self.total_count = 0
        self.failure_path = []

    def setup(self):   
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                if is_dicom(file):
                    dicom_path = os.path.join(root, file)
                    root_split = root.split('/')
                    if (len(root_split) < 3 or len(root_split) > 4):
                        raise FilePathException(root)
                    elif (len(root_split) == 4):
                        # subfolder contains Axial, Coronal or so on..
                        self.update_dicom_header(dicom_path, root_split)
                    elif (len(root_split) == 3):
                        root_split.append('Image')
                        self.update_dicom_header(dicom_path, root_split)
                        

    def update_dicom_header(self, dicom_path, info):
        if self.args.accession_number:
            print('change accession number')
        if self.args.patient_id:
            print('change patient id')
            print(info)
            patient_id = f'ILA{info[1]}' + "%03d" % 2     # generate new patient id
            
        if self.args.studies_id:
            print('change studies id')
        if self.args.series_description:
            print('change series description')


    def start(self):
        self.setup()



# def modify():
#     print('coming soon...')

# def app(args): 
#     # Recursively upload all .dcm files in dicom directory 
#     dicom_directory = args.dicom_directory[0]
#     storage = {}

#     if (args.studies_id or args.series_description):
#         modify()
#     else: 
#         # sort
#         for hospital in os.listdir(dicom_directory):
#             if (os.path.isdir(hospital)):
#                 # Make dict
#                 storage[hospital] = {}
#             else: 
#                 # ignore .DS_Store
#                 pass



#             # if is_dicom(file):
#             #     dicom_path = os.path.join(root, file)
#             #     try:
#             #         # overwrite_dicom_header(study_instance_uid_dict, dicom_path)
#             #         upload_dicom_image(dicom_path)
#             #     except OSError as err:
#             #         sys.stdout.write("OS error: {0}".format(err))
#             #     except:
#             #         sys.stdout.write("Unexpected error:", sys.exc_info()[0])


    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='**Dicom Manager**')
    parser.add_argument('--patient-id', '-pi',
                        action='store_true', help='change patients name/id')
    parser.add_argument('--studies-id', '-si',
                        action='store_true', help='change studies instance uid')
    parser.add_argument('--series-description', '-sd',
                        action='store_true', help='change series description')
    parser.add_argument('--accession-number', '-an',
                        action='store_true', help='change accession number')
    parser.add_argument('dicom_directory', type=str, nargs=1, metavar='<dicom directory>',
                        help='dicom directory')
    parser.add_argument('orthanc_username', type=str, nargs=1, metavar='<orthanc username>',
                        help='orthanc server username')
    parser.add_argument('orthanc_password', type=str, nargs=1, metavar='<orthanc password>',
                        help='orthanc server password')
    args = parser.parse_args()

    app = App(args)
    app.start()

