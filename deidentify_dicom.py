# Usage
# python 
#   deidentify_dicom.py 
#   /e/common/ImageData/DCM_20210827_GALA_RheSolve_STUDY00146630_TK/7071 
#   /e/common/ImageData/DCM_Deid_TK/GALA/127-06-003/20210827/
import os
import argparse
from pydicom import dcmread


# Create an argument parser
parser = argparse.ArgumentParser(
    description='Recursively de-identify and save DICOM images from src to dst')
parser.add_argument('src', metavar='src', type=str,
                    help='DICOM source folder path')
parser.add_argument('dst', metavar='dst', type=str,
                    help='DICOM destination folder path')
args = parser.parse_args()

src_dicom_dir = args.src
dst_dicom_dir = args.dst


def _get_dcm_paths_from_dir(dcm_dir: str):
    for base, _, files in os.walk(dcm_dir):
        for file in files:
            yield os.path.join(base, file)


def _deidentify_and_save_single_dicom_img(dcm_path: str, dst_dicom_dir: str):
    if dcm_path[-1] == '\\' or dcm_path[-1] == '/':
        dcm_path = dcm_path[:-1]
    if dst_dicom_dir[-1] == '\\' or dst_dicom_dir[-1] == '/':
        dst_dicom_dir = dst_dicom_dir[:-1]

    output_file_name = os.path.basename(dcm_path)
    output_dir_name = os.path.basename(os.path.dirname(dcm_path))
    patient_ID = os.path.basename(os.path.dirname(dst_dicom_dir))

    dicom_to_deidentify = dcmread(dcm_path)
    try:
        dicom_to_deidentify.PatientID = dicom_to_deidentify.PatientName = patient_ID
    except:
        print(f'{dcm_path}: PatientID or PatientName tag does not exist')

    tags_to_anonymize = [
        'PatientBirthDate', 
        'PatientSex', 
        'PatientAge',
        'InstitutionName',
        'InstitutionAddress',
        'InstitutionalDepartmentName',
        'ReferringPhysicianName',
        'ReferringPhysicianTelephoneNumbers',
        'ReferringPhysicianAddress',
        'PhysiciansOfRecord',
        'OperatorsName',
        'IssuerOfPatientID',
        'OtherPatientIDs',
        'OtherPatientNames',
        'OtherPatientIDsSequence',
        'PatientBirthName',
        'PatientSize',
        'PatientWeight',
        'PatientAddress',
        'PatientMotherBirthName',
        'CountryOfResidence',
        'RegionOfResidence',
        'CurrentPatientLocation',
        'PatientTelephoneNumbers',
        'SmokingStatus',
        'PregnancyStatus',
        'PatientReligiousPreference',
        'RequestingPhysician',
        'PerformingPhysicianName',
        'NameOfPhysiciansReadingStudy',
        'MilitaryRank',
        'EthnicGroup',
        'AdditionalPatientHistory',
        'PatientComments',
        'PersonName',
        'ScheduledPatientInstitutionResidence'
    ]
    for tag in tags_to_anonymize:
        if tag in dicom_to_deidentify:
            delattr(dicom_to_deidentify, tag)
    dicom_to_deidentify.remove_private_tags()
    
    if not os.path.exists(f'{dst_dicom_dir}/{output_dir_name}'):
        os.makedirs(f'{dst_dicom_dir}/{output_dir_name}')
    dicom_to_deidentify.save_as(f'{dst_dicom_dir}/{output_dir_name}/{output_file_name}')
    return


if __name__ == "__main__":
    for dcm_path in _get_dcm_paths_from_dir(src_dicom_dir):
        _deidentify_and_save_single_dicom_img(dcm_path, dst_dicom_dir)