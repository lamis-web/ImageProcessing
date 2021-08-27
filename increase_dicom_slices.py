import numpy as np
import copy
from pydicom import dcmread
from typing import List
import os


def _get_dcm_paths_from_dir(dicom_dir: str):
    for base, dirs, files in os.walk(dicom_dir):
        for file in files:
            yield os.path.join(base, file)


def check_dcm_header(dcm):
    print(dcm.InstanceNumber, dcm.SOPInstanceUID, dcm.LargestImagePixelValue, dcm[0x00200032])


def construct_slices(dicom_dir: str, extended_pixel_array=None):
    for dcm_path in _get_dcm_paths_from_dir(dicom_dir):
        dcm = dcmread(dcm_path)
        check_dcm_header(dcm)


if __name__ == '__main__':
    construct_slices('Data/SampleDicom/1393/dicom')
    # ds = dcmread(r"Data\SampleDicom\1393\dicom\1.3.12.2.1107.5.1.4.65305.30000020091412370754200016817.dcm")
    # print(ds.pixel_array.shape)
# print(ds1.pixel_array)
# print(ds1.pixel_array.shape)
# temp_array = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
# ds1.PixelData = temp_array.tobytes()
# print(ds1.PixelData)
# print(ds1.pixel_array)
# print(ds1.pixel_array.shape)

# ds1 = dcmread(
#     "Data/SampleDicom/1393/dicom/1.3.12.2.1107.5.1.4.65305.30000020091412370754200016784.dcm"
# )

# ds2 = copy.deepcopy(ds1)
# print(id(ds1))
# print(id(ds2))