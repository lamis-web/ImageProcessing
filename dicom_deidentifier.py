# ##############################################################################
# Usage: python dicom_deidentifier.py {dicom_path} {out_path} {subjID} {imgID}
# Run Time: <10s
# Ref:
# ##############################################################################
# Desc: copy dicom from dicom_path to out_path and change metadata
# ##############################################################################

from pydicom import dcmread
from pydicom.datadict import dictionary_VR
from random import randint
import os
import sys
import shutil
import logging

# src_dicom_path = '/Users/inkyu/Desktop/SNUH/data/177/dicom'
# output_path = '/Users/inkyu/Desktop/SNUH/data/177/dicom2'
# subj_ID = 'PMSN00000'
# img_ID = 'IN0'

src_dicom_path = str(sys.argv[1])
output_path = str(sys.argv[2])
subj_ID = str(sys.argv[3])
img_ID = str(sys.argv[4])

# Create a logger
logging.basicConfig(filename='dicom_deidentifier.log', level=logging.WARNING,
                    filemode='a', format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Prepare a output folder
out_subj_path = os.path.join(output_path, f'{subj_ID}_{img_ID}')
if not os.path.exists(out_subj_path):
    os.makedirs(out_subj_path)

# Copy
out_dicom_folder_path = os.path.join(out_subj_path, 'dicom')
if not os.path.exists(out_dicom_folder_path):
    shutil.copytree(src_dicom_path, out_dicom_folder_path)

# Overwrite
dicom_paths = [os.path.join(out_dicom_folder_path, dcm)
               for dcm in os.listdir(out_dicom_folder_path)]
for dicom_path in dicom_paths:
    dicom_instance = dcmread(dicom_path)

    if dicom_instance.get('PatientName'):
        dicom_instance.PatientName = subj_ID
        logger.info(f'{dicom_path} - PatientName Header Processed')
    else:
        logger.error(f'{dicom_path} - PatientName Header does not exist')
        continue

    if dicom_instance.get('PatientID'):
        dicom_instance.PatientID = subj_ID
        logger.info(f'{dicom_path} - PatientID Header Processed')
    else:
        logger.error(f'{dicom_path} - PatientID Header does not exist')
        continue

    if dicom_instance.get('PatientBirthDate'):
        dicom_instance.PatientBirthDate = str(
            int(dicom_instance.PatientBirthDate) + (randint(1, 500) * 10000))
        logger.info(f'{dicom_path} - PatientBirthDate Header Processed')
    else:
        logger.warning(
            f'{dicom_path} - PatientBirthDate Header does not exist')

    if dicom_instance.get('AccessionNumber'):
        dicom_instance.AccessionNumber = subj_ID + "_" + img_ID
        logger.info(f'{dicom_path} - AccessionNumber Header Processed')
    else:
        logger.warning(
            f'{dicom_path} - AccessionNumber Header does not exist: Appending Header')
        dicom_instance.add_new([0x0008, 0x0050], dictionary_VR(
            [0x0008, 0x0050]), subj_ID + "_" + img_ID)

    if dicom_instance.get('StudyDate'):
        dicom_instance.StudyDate = str(
            int(dicom_instance.StudyDate) + (randint(1, 30)))
        logger.info(f'{dicom_path} - StudyDate Header Processed')
    else:
        logger.error(f'{dicom_path} - StudyDate Header does not exist')
        continue

    if dicom_instance.get('SeriesDate'):
        dicom_instance.SeriesDate = dicom_instance.StudyDate
    else:
        logger.warning(
            f'{dicom_path} - SeriesDate Header does not exist: Appending Header')
        dicom_instance.add_new([0x0008, 0x0021], dictionary_VR(
            [0x0008, 0x0021]), dicom_instance.StudyDate)

    if dicom_instance.get('AcquisitionDate'):
        dicom_instance.AcquisitionDate = dicom_instance.StudyDate
    else:
        logger.warning(
            f'{dicom_path} - AcquisitionDate Header does not exist: Appending Header')
        dicom_instance.add_new([0x0008, 0x0022], dictionary_VR(
            [0x0008, 0x0022]), dicom_instance.StudyDate)

    if dicom_instance.get('ContentDate'):
        dicom_instance.ContentDate = dicom_instance.ContentDate
    else:
        logger.warning(
            f'{dicom_path} - ContentDate Header does not exist: Appending Header')
        dicom_instance.add_new([0x0008, 0x0023], dictionary_VR(
            [0x0008, 0x0023]), dicom_instance.StudyDate)

    # Change all metadata here #
    # dicom_instance.StudyInstanceUID
    # dicom_instance.SeriesInstanceUID
    # dicom_instance.SOPInstanceUID
    # dicom_instance.StudyDescription
    # dicom_instance.SeriesDescription

    # Sanitize all metadata here #
    # dicom_instance.OverlayDate
    # dicom_instance.CurveDate
    # dicom_instance.AcquisitionDatetime
    # dicom_instance.StudyTime
    # dicom_instance.SeriesTime
    # dicom_instance.AcquisitionTime
    # dicom_instance.ContentTime
    # dicom_instance.OverlayTime
    # dicom_instance.CurveTime
    # dicom_instance.InstitutionName
    # dicom_instance.InstitutionAddress
    # dicom_instance.ReferringPhysiciansName
    # dicom_instance.ReferringPhysiciansAddress
    # dicom_instance.ReferringPhysiciansTelephoneNumber
    # dicom_instance.ReferringPhysicianIDSequence
    # dicom_instance.InstitutionalDepartmentName
    # dicom_instance.PhysicianOfRecord
    # dicom_instance.PhysicianOfRecordIDSequence
    # dicom_instance.PerformingPhysiciansName
    # dicom_instance.PerformingPhysicianIDSequence
    # dicom_instance.NameOfPhysicianReadingStudy
    # dicom_instance.PhysicianReadingStudyIDSequence
    # dicom_instance.OperatorsName
    # dicom_instance.IssuerOfPatientID
    # dicom_instance.PatientSex
    # dicom_instance.OtherPatientIDs
    # dicom_instance.OtherPatientNames
    # dicom_instance.PatientsBirthName
    # dicom_instance.PatientAge
    # dicom_instance.PatientAddress
    # dicom_instance.PatientMothersBirthName
    # dicom_instance.CountryOfResidence
    # dicom_instance.RegionOfResidence
    # dicom_instance.PatientTelephoneNumbers
    # dicom_instance.StudyID
    # dicom_instance.CurrentPatientLocation
    # dicom_instance.PatientInstitutionResidence
    # dicom_instance.DateTime
    # dicom_instance.Date
    # dicom_instance.Time
    # dicom_instance.PersonName

    dicom_instance.save_as(dicom_path)
