# Orhtanc Manager
#
# orthanc manager is the python script which enable the users to
# delete, modify the multiple data using python script.
# Since web UI (https://localhost:8042) only deletes the data one by one,
# this python script will make modifying job much faster.

import pydicom
# pip install requests, only available in /data7/common/dkang0602venvs/dicom/bin
import requests
import argparse
from progress.bar import IncrementalBar

URL = 'http://localhost:8042/'

# Exception
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





def delete(patients, studies):
    '''
    patients -> patient_storage | the hashed key of patients that needs to be deleted.
    studies -> studies_storage  |           "       studies         " .
    '''
    total   = len(patients) + len(studies)
    success = 0
    bar = IncrementalBar('Deleting ...', max=total)
    
    for p in patients:
        request_patients = requests.delete(URL + 'patients/' + p)
        if (request_patients.status_code != 200):
            # raise OrthancRequestException(request_patients.status_code)
            pass
        else:
            success += 1
        bar.next()
    
    for s in studies:
        request_studies = request.delete(URL + 'studies/' + s) 
        if (request_studies.status_code != 200):
            # raise OrthancRequestException(request_patients.status_code)
            pass
        else:
            success += 1
        bar.next()

    bar.finish()
    print(f'DELETE COMPLETE !!! [{success}/{total}]')

def scan(patients, studies):
    # patient
    request_patients = requests.get(URL + 'patients')
    request_studies = requests.get(URL + 'studies')
    if (request_patients.status_code != 200):
        raise OrthancRequestException(request_patients.status_code)
    if (request_studies.status_code != 200):
        raise OrthancRequestException(request_patients.status_code)
    else:
        p_list = request_patients.json()
        s_list = request_studies.json()
        bar = IncrementalBar('Searching... ', max=len(p_list) + len(s_list))
        patients_storage = []                       # PATIENTS THAT NEEDS TO BE DELETED
        studies_storage  = []
        # Find the encrypted code of the patients
        for p in p_list:
            request_patient_data = requests.get(URL + 'patients/' + p)
            if (request_patient_data.status_code != 200):
                raise OrthancRequestException(request_patient_data.status_code)
            else:
                patient_data = request_patient_data.json()
                p_id = patient_data['MainDicomTags']['PatientID'] 
                p_name = patient_data['MainDicomTags']['PatientName']
                if (p_id != p_name):
                    # raise OrthancIdNameMatchException(p_id, p_name)
                    pass
                else:
                    if patients == None:
                        pass
                    else:
                        for patient in patients:
                            # search the patients that needs to be deleted
                            if patient.lower() in p_id.lower():
                                # patient_data that needs to be deleted.  
                                patients_storage.append(p)       
            bar.next()
        # Find the encrypted code of the studies
        for s in s_list:
            request_study_data = requests.get(URL + 'studies/' + s)
            if (request_study_data.status_code != 200):
                raise OrthancRequestException(request_study_data.status_code)
            else:
                study_data = request_study_data.json()
                s_id = study_data['MainDicomTags']['StudyInstanceUID']
                if studies == None:
                    pass
                else:
                    for study in studies:
                        # search the patients that needs to be deleted
                        if study in s_id:
                            # patient_data that needs to be deleted.  
                            studies_storage.append(s)       
            bar.next()
        bar.finish()
        
        # Ask users to continue
        print(f"Found {len(studies_storage) + len(patients_storage)} to delete...")
        while (True):
            cont = input('Do you really wish to continue? [Y/n]: ')
            if cont.lower() == 'y':
                delete(patients_storage, studies_storage)       # DELETING STARTS HERE
                break
            elif cont.lower() == 'n':
                exit()
                


def info(patients, studies):
    print("Info coming soon...")




# MAIN
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Orthanc Manager')
    parser.add_argument('--patients', '-p', nargs='+',
                        help='get all the instances from orthanc server')
    parser.add_argument('--studies', '-i', nargs='+',
                        help='get all the instances from orthanc server')
    # parser.add_argument('--command', choices=['delete', 'info'],
    #                     help='Choose what task to do')

    args = parser.parse_args()
    patients_list = args.patients
    studies_list = args.studies
    scan(patients_list, studies_list)
