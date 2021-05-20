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
import time

# GLOBAL VARIABLE
HOST_URL = '127.0.0.1'
ORTHANC_PORT = 8042
ORTHANC_URL = 'http://%s:%d/' % (HOST_URL, ORTHANC_PORT)
PULMORAD_ROOT_UID = '1.2.826.0.1.3680043.8.499.'

# Exception


class FilePathException(Exception):
    '''
    Exception raised when the file does not start in ImageData_KSTR
    '''

    def __init__(self, root):
        self.root = root

    def __str__(self):
        return f' -> Folder Path has to be in ImageData_KSTR. Occurred in {self.root}'


class OrthancRequestException(Exception):
    '''
    Exception raised when the orthanc request fails.
    '''

    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return 'Cannot connect to Orthanc server. CODE: ' + str(self.status_code)


class OrthancIdNameMatchException(Exception):
    '''
    Exception raised when the Patient Id and Name do not match.
    '''

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f'Orthanc Server has the data that Patient ID and Patient Name does not match\nID   : {self.id}\nName : {self.name}\nIt is better to fix the issue first rather than deleting'


# HELPERS
def is_dicom(file):
    '''
    check whether the file is dicom file or not .dcm .DCM
    '''
    file_extension = file.split('.')[-1]
    return file_extension == 'dcm' or file_extension == 'DCM'


def get_patient_number(patient_id):
    '''
    Set patient number with patient id / name
    '''
    return int(''.join(i for i in patient_id if i.isdigit()))


def proceed():
    '''
    fn: Ask users to continue with the process
    '''
    while (True):
        cont = input('Do you really wish to continue? [Y/n]: ')
        if cont.lower() == 'y':
            return True
            break
        elif cont.lower() == 'n':
            exit()

def push_proceed():
    '''
    fn: Ask users to continue with the process
    '''
    while (True):
        print('WARNING - This might cause collision when there are same Patient/Studies in orthanc server')
        cont = input('Do you really wish to continue? [Y/n]: ')
        if cont.lower() == 'y':
            return True
            break
        elif cont.lower() == 'n':
            exit()

# APPLICATION
class App:
    def __init__(self, args):
        self.args = args                                # argument
        # directory that is working on
        self.dir = args.dicom_directory[0]
        self.success_count = 0
        self.failure_count = 0
        self.total_count = 0
        self.dicom_count = 0
        self.failure_path = []
        self.is_update = self.args.accession_number or self.args.patient_id or self.args.studies_id or self.args.series_description
        self.is_push = self.args.push

        self.patient_list = []
        self.studies_list = []
        self.series_list = []
        self.instances_list = []

    def get_orthanc_data(self):

        request_pid = requests.get(ORTHANC_URL + 'patients')
        request_sid = requests.get(ORTHANC_URL + 'studies')
        request_ssid = requests.get(ORTHANC_URL + 'series')
        request_iid = requests.get(ORTHANC_URL + 'instances')

        if (request_pid.status_code != 200):
            raise OrthancRequestException(request_pid.status_code)
        if (request_sid.status_code != 200):
            raise OrthancRequestException(request_sid.status_code)
        if (request_ssid.status_code != 200):
            raise OrthancRequestException(request_ssid.status_code)
        if (request_iid.status_code != 200):
            raise OrthancRequestException(request_iid.status_code)

        hashed_patients_list = request_pid.json()
        hashed_studies_list = request_sid.json()
        hashed_series_list = request_ssid.json()
        hashed_instances_list = request_iid.json()

        total_count = len(hashed_patients_list) + len(hashed_instances_list) + \
            len(hashed_series_list) + len(hashed_studies_list)

        with IncrementalBar('\n>>> Fetching data from orthanc ... ', max=total_count, suffix='%(percent).1f%% - %(eta)ds') as bar:
            for patient in hashed_patients_list:
                p = requests.get(ORTHANC_URL + '/patients/' + patient)
                if (p.status_code != 200):
                    raise OrthancRequestException(p.status_code)
                patient_info = p.json()
                self.patient_list.append(
                    patient_info['MainDicomTags']['PatientID'])
                bar.next()
            for studies in hashed_studies_list:
                s = requests.get(ORTHANC_URL + '/studies/' + studies)
                if (s.status_code != 200):
                    raise OrthancRequestException(s.status_code)
                study_info = s.json()
                self.studies_list.append(
                    study_info['MainDicomTags']['StudyInstanceUID'])
                bar.next()
            for series in hashed_series_list:
                ss = requests.get(ORTHANC_URL + '/series/' + series)
                if (ss.status_code != 200):
                    raise OrthancRequestException(ss.status_code)
                series_info = ss.json()
                self.series_list.append(
                    series_info['MainDicomTags']['SeriesInstanceUID'])
                bar.next()
            for instances in hashed_instances_list:
                i = requests.get(ORTHANC_URL + '/instances/' + instances)
                if (i.status_code != 200):
                    raise OrthancRequestException(i.status_code)
                instances_info = i.json()
                self.instances_list.append(
                    instances_info['MainDicomTags']['SOPInstanceUID'])
                bar.next()
        print(f'Orthanc Server has ...')
        print(f'\tPatients   : {len(self.patient_list)}')
        print(f'\tStudies    : {len(self.studies_list)}')
        print(f'\tSeries     : {len(self.series_list)}')
        print(f'\tInstances  : {len(self.instances_list)}')


    def update_dicom_header(self, dicom_path, info):
        ds = dcmread(dicom_path)

        if self.args.accession_number:
            # update accession number
            patient_num = get_patient_number(info[2])
            # generate new patient id
            patient_id = f'ILA{info[1]}' + "%04d" % patient_num
            ds.AccessionNumber = patient_id + '_IN0'
            # Accession Number --> _IN0cor / _IN0axi
        if self.args.patient_id:
            # update patient id / name
            patient_num = get_patient_number(info[2])
            # generate new patient id
            patient_id = f'ILA{info[1]}' + "%04d" % patient_num
            ds.PatientID = patient_id
            ds.PatientName = patient_id
        if self.args.studies_id:
            # update studies id
            pass
        if self.args.series_description:
            # update series description
            if info[3] == 'Image':
                series_description = ds.SeriesDescription.split(' - ')[0]
            else:
                # ex) SERIES03 - Axial // SERIES03 - Coronal
                series_description = ds.SeriesDescription.split(
                    ' - ')[0] + ' - ' + info[3]
            ds.SeriesDescription = series_description
        print(dicom_path)
        ds.save_as(dicom_path)

    # def check_uploaded(self, file):
    #   TODO: check patient if the item is uploaded
    #   for now, orthanc server only deals with patients, studiesid
    #   updated needed.

    def update(self):
        '''
        function updates the dicom header.
        '''
        bar = IncrementalBar(
            f'>>> {self.dicom_count} Dicom header is updating ... ', max=self.dicom_count)
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                if is_dicom(file):
                    dicom_path = os.path.join(root, file)
                    root_split = root.split('/')
                    if (len(root_split) < 3 or len(root_split) > 4):
                        # subfolder의 갯수를 정해놓는다. ImageData_KSTR/XX/ILAXX/(Axial/Coronal)/xxx.dcm
                        raise FilePathException(dicom_path)
                    elif (len(root_split) == 4):
                        # subfolder contains Axial, Coronal or so on..
                        self.update_dicom_header(dicom_path, root_split)
                    elif (len(root_split) == 3):
                        root_split.append('Image')
                        self.update_dicom_header(dicom_path, root_split)
                    bar.next()
        bar.finish()

    def upload_dicom_image(self, dicom_path: str):
        """[Upload single instance of DICOM image(.dcm)]

        Args:
            dicom_path ([str]): [path to the single DICOM image]
        """
        with open(dicom_path, 'rb') as dicom_image:
            content = dicom_image.read()

            try:
                # sys.stdout.write("Importing %s" % dicom_path)
                h = httplib2.Http()
                headers = {'content-type': 'application/dicom'}

                username = self.orthanc_username
                password = self.orthanc_password
                creds_str = username + ':' + password
                creds_str_bytes = creds_str.encode("ascii")
                creds_str_bytes_b64 = b'Basic ' + base64.b64encode(creds_str_bytes)
                headers['authorization'] = creds_str_bytes_b64.decode("ascii")

                response, content = h.request(
                    ORTHANC_URL+'/instances', 'POST', body=content, headers=headers)

                if response.status != 200:
                    print('Unable to push ==> ' + dicom_path)

            except:
                print('Unable to connect..')
                exit()


    def push(self):
        '''
        function push the data to the orthanc server
        '''
        
        with IncrementalBar('>>> Uploading to Orthanc Server ... ', max=self.dicom_count, suffix='%(percent).1f%% - %(eta)ds') as bar:
            for root, dirs, files in os.walk(self.dir):
                for file in files:
                    if is_dicom(file):
                        dicom_path = os.path.join(root, file)
                        # self.check_uploaded(dicom_path)
                        try:
                            # overwrite_dicom_header(study_instance_uid_dict, dicom_path)
                            self.upload_dicom_image(dicom_path)
                        except OSError as err:
                            sys.stdout.write("OS error: {0}".format(err))
                        except:
                            sys.stdout.write("Unexpected error:", sys.exc_info()[0])
                        bar.next()

    def start(self):
        # self.get_orthanc_data()
        self.orthanc_username = self.args.orthanc_username[0]
        self.orthanc_password = self.args.orthanc_password[0]

        for root, dirs, files in os.walk('.'):
            for file in files:
                if is_dicom(file):
                    self.dicom_count += 1
        if self.is_update:
            self.update()
        if self.is_push:
            if push_proceed():       # ask again if user really wants to push
                self.push()
        print('\nDONE!!!')


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
    parser.add_argument('--push', '-p',
                        action='store_true', help='upload to orthanc server')
    parser.add_argument('dicom_directory', type=str, nargs=1, metavar='<dicom directory>',
                        help='dicom directory')
    parser.add_argument('orthanc_username', type=str, nargs=1, metavar='<orthanc username>',
                        help='orthanc server username')
    parser.add_argument('orthanc_password', type=str, nargs=1, metavar='<orthanc password>',
                        help='orthanc server password')
    args = parser.parse_args()

    app = App(args)
    app.start()
