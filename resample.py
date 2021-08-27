import numpy as np
import scipy.ndimage

def resample(img, spacing, new_spacing=[1,1,1]):
    spacing = np.array(spacing, dtype=np.float32)
    resize_factor = spacing / new_spacing
    new_real_shape = img.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / img.shape
    new_spacing = spacing / real_resize_factor
    # Cubic spline, nearest neighbor for the boundary
    img = scipy.ndimage.interpolation.zoom(img,real_resize_factor, mode='nearest')
    return img


def test():
    img = np.ones((512,512,100))
    print(f'Before Resampling: {img.shape}')
    spacing = [1,1,2]
    new_spacing = [1,1,1]
    # Convert 1x1x2mm spacing to 1x1x1mm spacing
    img = resample(img,spacing,new_spacing)
    print(f'After Resampling: {img.shape}')

if __name__ == '__main__':
    test()
