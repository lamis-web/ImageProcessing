import numpy as np
import scipy.ndimage
import copy
from pydicom import dcmread, FileDataset, Dataset
from typing import List, Tuple
import os

# from medpy.io import save, load

# class DCM_header():
#     def __init__(self):
        
#         self.PixelSpacing = [2,3]

def _get_dcm_paths_from_dir(dcm_dir: str) -> List[str]:
    paths = []
    for base, dirs, files in os.walk(dcm_dir):
        for file in files:
            paths.append(os.path.join(base, file))
    return paths


def _check_dataset(dicom_dir: str):
    for dcm_path in _get_dcm_paths_from_dir(dicom_dir):
        dcm = dcmread(dcm_path)
        print(dcm_path.split(''))
        print(
            dcm.InstanceNumber,
            # dcm.SOPInstanceUID,
            dcm.Rows,
            dcm.Columns,
            dcm.LargestImagePixelValue,
            dcm.ImagePositionPatient,
            dcm.SliceLocation,
            dcm.PixelSpacing
        )


def _read_dcm_dataset(dcm_dir: str) -> Tuple[List[Dataset], np.ndarray]:
    dcm_paths = _get_dcm_paths_from_dir(dcm_dir)
    dcm_dataset = [dcmread(dcm_path) for dcm_path in dcm_paths]
    dcm_spacing = list(map(lambda x : np.float16(x), [*dcm_dataset[0].PixelSpacing, dcm_dataset[0].SliceThickness]))
    dcm_pixel_array = np.transpose(np.array([dcm_data.pixel_array for dcm_data in dcm_dataset]), (1,2,0))

    return dcm_dataset, dcm_spacing, dcm_pixel_array


def _resample_dcm_pixel_array(img: np.ndarray, spacing: List[np.float16], new_spacing: List[np.float16]) -> np.ndarray:
    spacing = np.array(spacing, dtype=np.float16)
    resize_factor = spacing / new_spacing
    new_real_shape = img.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / img.shape
    new_spacing = spacing / real_resize_factor
    # Cubic spline, nearest neighbor for the boundary
    img = scipy.ndimage.interpolation.zoom(img, real_resize_factor, mode="nearest")
    # return np.array(img, dtype=np.float16)
    return img


def _construct_new_dcm_slice(
    dcm_template: Dataset, new_spacing: np.float16, instance_number: int, resampled_dcm_pixel_2D: np.ndarray
) -> Dataset:
    new_dcm_slice = copy.deepcopy(dcm_template)
    new_dcm_slice.InstanceNumber = instance_number
    new_dcm_slice.SliceLocation = new_dcm_slice.SliceLocation - new_spacing * (instance_number - 1)
    new_dcm_slice.ImagePositionPatient[2] = new_dcm_slice.SliceLocation
    new_dcm_slice.SliceThickness = new_spacing
    new_dcm_slice.PixelData = resampled_dcm_pixel_2D.tobytes()
    print(new_dcm_slice.InstanceNumber, new_dcm_slice.SliceLocation, new_dcm_slice.ImagePositionPatient)
    return new_dcm_slice

def _construct_and_save_new_dcm_dataset(dcm_dataset: List[Dataset], new_spacing: np.float16, resampled_dcm_pixel_array: np.ndarray, output_path: str) -> FileDataset:
    dcm_template = dcm_dataset[0]
    resampled_dcm_pixel_array = np.transpose(resampled_dcm_pixel_array, (2,0,1)).astype(np.uint16)
    for i, dcm_slice in enumerate(dcm_dataset):
        LargestImagePixelValue = np.unique(resampled_dcm_pixel_array[i])[-1]
        dcm_slice.LargestImagePixelValue = LargestImagePixelValue
        dcm_slice.PixelData = resampled_dcm_pixel_array[i].tostring()
        dcm_slice.save_as(f'{output_path}/{i}.dcm')

def resample_dcm(
    dcm_dir: str, new_spacing=1.0, output_path="Output/dicom"
):
    dcm_dataset, dcm_spacing, dcm_pixel_array = _read_dcm_dataset(dcm_dir)
    new_dcm_spacing = [*dcm_spacing[:-1], new_spacing]
    resampled_dcm_pixel_array = _resample_dcm_pixel_array(dcm_pixel_array, dcm_spacing, new_dcm_spacing)
    _construct_and_save_new_dcm_dataset(dcm_dataset, new_spacing, resampled_dcm_pixel_array, output_path)

if __name__ == "__main__":
    resample_dcm("Data/SampleDicom/1393/dicom")
    # _check_dataset("Data/SampleDicom/1393/dicom")
    # _check_dataset("Output/dicom")