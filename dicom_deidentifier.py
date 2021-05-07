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
    # dicom_instance.PatientID
    # dicom_instance.AccessionNumber
    # dicom_instance.StudyInstanceUID
    # dicom_instance.SeriesInstanceUID
    # dicom_instance.SOPInstanceUID
    # dicom_instance.StudyDescription
    # dicom_instance.SeriesDescription
    
    # Sanitize all metadata here #
    # dicom_instance.StudyDate
    # dicom_instance.SeriesDate
    # dicom_instance.AcquisitionDate
    # dicom_instance.ContentDate
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
    # dicom_instance.PatientBirthDate
    # dicom_instance.PatientBirthTime
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