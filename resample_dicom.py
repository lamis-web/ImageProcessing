import numpy as np
import scipy.ndimage
import copy
from pydicom import dcmread, FileDataset
from typing import List
import os


def _get_dcm_paths_from_dir(dicom_dir: str) -> List[str]:
    paths = []
    for base, dirs, files in os.walk(dicom_dir):
        for file in files:
            paths.append(os.path.join(base, file))
    return paths


def _check_dataset(dicom_dir: str):
    for dcm_path in _get_dcm_paths_from_dir(dicom_dir):
        dcm = dcmread(dcm_path)
        print(
            dcm.InstanceNumber,
            dcm.SOPInstanceUID,
            dcm.LargestImagePixelValue,
            dcm.ImagePositionPatient,
            dcm.SliceLocation,
        )


def _resample(img, spacing, new_spacing=[1, 1, 1]):
    spacing = np.array(spacing, dtype=np.float32)
    resize_factor = spacing / new_spacing
    new_real_shape = img.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / img.shape
    new_spacing = spacing / real_resize_factor
    # Cubic spline, nearest neighbor for the boundary
    img = scipy.ndimage.interpolation.zoom(img, real_resize_factor, mode="nearest")
    return img


def _construct_new_slice(
    dcm: FileDataset, instance_number: int, pixel_array: np.ndarray = None
) -> FileDataset:
    new_dcm = copy.deepcopy(dcm)
    new_dcm.InstanceNumber = instance_number
    return new_dcm


def construct_new_dataset(
    dicom_dir: str, extended_pixel_array=None, output_path="Output/dicom"
):
    for i, dcm_path in enumerate(_get_dcm_paths_from_dir(dicom_dir), 1):
        # read & modify InstanceNumber & save original dicom slices
        # instance_number += 1

        # dcm = dcmread(dcm_path)
        # dcm.InstanceNumber = instance_number
        # dcm.save_as(f'{output_path}/{instance_number}.dcm')

        # # create & save new dicom slices
        # instance_number += 1
        # dcm_created = _construct_new_slice(dcm, instance_number)
        # dcm_created.save_as(f'{output_path}/{instance_number}.dcm')

        # _check_some_dcm_header(dcm)
        pass


if __name__ == "__main__":
    # construct_new_dataset("Data/SampleDicom/1393/dicom")
    # _check_dataset('Output/dicom')

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
