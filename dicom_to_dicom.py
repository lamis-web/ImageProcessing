import numpy as np
from pydicom import dcmread

ds1 = dcmread(
    "/home/twkim/work/kumc/image-processing/Data/SampleDicom/1.3.6.1.4.1.25403.220837857011494.5380.20210609114039.1.dcm"
)

ds2 = dcmread("/home/twkim/work/kumc/image-processing/Data/SampleDicom/temp.dcm")
# print(ds1)
print(ds1.pixel_array)
print(ds1.pixel_array.shape)
temp_array = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
ds1.PixelData = temp_array.tobytes()
print(ds1.PixelData)
print(ds1.pixel_array)
print(ds1.pixel_array.shape)
