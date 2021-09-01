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
    output_dir_name = dcm_path.split('\\')[-2] if dcm_path.split('\\') != [] else dcm_path.split('/')[-2]
    output_file_name = dcm_path.split('\\')[-1] if dcm_path.split('\\') != [] else dcm_path.split('/')[-1]
    
    dicom_to_deidentify = dcmread(dcm_path)
    try:
        dicom_to_deidentify.PatientID = dicom_to_deidentify.PatientName = output_dir_name
    except:
        print(f'{dcm_path}: PatientID or PatientName tag does not exist')

    tags_to_anonymize = ['PatientBirthDate', 'PatientSex', 'PatientAge']
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