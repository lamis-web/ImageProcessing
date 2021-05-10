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

URL = 'http://localhost:8042/'


def get_hospital_name(name: str):
    # param: name ==> 'XX'
    # find all the name contains XX -->XX  'ILAXX000'

    print ("get_hospital_name")
    # def app():

def delete(patients, studies):
    print("Deleting starts,")

    # patient
    request_patients = requests.get(URL + 'patients')
    if (request_patients.status_code != 200):
        print("ERR: Cannot fetch the data from " + URL + 'patients')
        exit()
    else:
        encrypted_patient_list = request_patients.json()
        for e_patient in encrypted_patient_list:
            try:
                patient_data = requests.get(URL + 'patients/' + e_patient).json()
                break
            except:
                print("ERR: Cannot fetch the data from " + URL + 'patients/<ENCODE>')
                exit()




def info(patients, studies):
    print("Info coming soon...")


def app(command, patients, studies):
    # command: 'delete' / 'info'
    # patients: list of patient ID/Name that needs to be modified
    # studies : list of studies that needs to be modified
    print(command)
    print(patients)
    print(studies)
    if (command == 'delete'):
        delete(patients, studies)
    else:
        info(patients, studies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--patients', '-p', nargs='+',
                        help='get all the instances from orthanc server')
    parser.add_argument('--studies', '-i', nargs='+',
                        help='get all the instances from orthanc server')
    parser.add_argument('--command', choices=['delete', 'info'],
                        help='Choose what task to do')

    args = parser.parse_args()

    app(args.command, args.patients, args.studies)

# response_instances = requests.get(URL + 'instances')
# response_patients = requests.get(URL + 'patients')
# response_changes = requests.get(URL + 'changes')
# response_studies = requests.get(URL + 'studies')
# response_series = requests.get(URL + 'series')

# responded = response_changes.status_code == 200 and response_instances.status_code == 200 and response_patients.status_code == 200 and response_studies.status_code == 200 and response_series.status_code == 200

# if (responded):
#     # success
#     print('Instances  : ' + str(len(response_instances.json())) + '개')
#     print('Patients   : ' + str(len(response_patients.json())) + '개')
#     print('Changes    : ' + str(len(response_changes.json())) + '개')
#     print('Studies    : ' + str(len(response_studies.json())) + '개')
#     print('Series     : ' + str(len(response_series.json())) + '개')

#     app()
#     # for i, encrypted, in enumerate(response.json()):
#     # print(i, encrypted)
# else:
#     print('ERR: Network error occurred when connecting to orthanc server')
#     err_str = ''
#     if (response_instances.status != 200): err_str += 'Instances  '
#     if (response_patients.status != 200): err_str += 'Patients  '
#     if (response_changes.status != 200): err_str += 'Changes  '
#     if (response_studies.status != 200): err_str += 'Studies  '
#     if (response_series.status != 200): err_str += 'Series  '
#     print('     -> ' + err_str)
#     exit()
