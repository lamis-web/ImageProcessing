# ##############################################################################
# Usage: python dicom_deidentifier.py {dicom_path} {out_path} {subjID} {imgID}
# Run Time: <10s
# Ref: 
# ##############################################################################
# Desc: copy dicom from dicom_path to out_path and change metadata
# ##############################################################################

from pydicom import dcmread
import os
import sys
import shutil

# src_dicom_path = '/Users/inkyu/Desktop/SNUH/data/177/dicom'
# output_path = '/Users/inkyu/Desktop/SNUH/data/177/dicom2'
# subj_ID = 'PMSN00000'
# img_ID = 'IN0'

src_dicom_path = str(sys.argv[1])
output_path = str(sys.argv[2])
subj_ID = str(sys.argv[3])
img_ID = str(sys.argv[4])

# Prepare a output folder
out_subj_path = os.path.join(output_path,f'{subj_ID}_{img_ID}')
if not os.path.exists(out_subj_path):
    os.makedirs(out_subj_path)
# Copy
out_dicom_folder_path = os.path.join(out_subj_path,'dicom')
if not os.path.exists(out_dicom_folder_path):
    shutil.copytree(src_dicom_path,out_dicom_folder_path)

# Overwrite
dicom_paths = [os.path.join(out_dicom_folder_path,dcm) for dcm in os.listdir(out_dicom_folder_path)]
for dicom_path in dicom_paths:
    dicom_instance = dcmread(dicom_path)
    dicom_instance.PatientName = subj_ID
    # Change all metadata here #

    # dicom_instance.StudyInstanceUID
    # dicom_instance.SeriesDescription

    dicom_instance.save_as(dicom_path)