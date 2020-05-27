import numpy as np
from scipy import misc, ndimage
from time import time
import torch
import argparse
import SimpleITK as sitk


# This is a test

def timer(func):
    def f(*args, **kwargs):
        before = time()
        rv = func(*args, **kwargs)
        after = time()
        print("function", func.__name__, "taken", after - before)
        return rv
    return f


@timer
def torchGetBoundary(mask, boundary_width):
    max_pool = torch.nn.MaxPool3d(boundary_width, 1)
    avg_pool = torch.nn.AvgPool3d(boundary_width, 1)
    return max_pool(mask) - avg_pool(mask)


@timer
def getBoundary(mask, boundary_width):
    assert boundary_width % 2 == 1, "Boundary width should be odd number, now getting {}".format(
        boundary_width)
    mask = np.pad(mask.astype(np.float), (boundary_width)//2)
    mask = torch.unsqueeze(torch.from_numpy(mask), 0)
    edge = torchGetBoundary(mask, boundary_width)
    binarized = torch.squeeze((edge > 0))
    return binarized.numpy().astype(np.int_)


@timer
def _gaussian(edge, nn):
    return ndimage.gaussian_filter(edge, sigma=nn*2+1)


@timer
def _sobel3D(mask):
    return ndimage.sobel(mask, 1)+ndimage.sobel(mask, 2)+ndimage.sobel(mask, 0)


@timer
def getBoundarySobel(mask, extend_edge=False, nn=1):
    edge = _sobel3D(mask)
    if extend_edge:
        edge = _gaussian(edge, nn)
    binarized_boundary = (edge > 0).astype(np.int_)
    return binarized_boundary


def get_args():
    parser = argparse.ArgumentParser(description='input the filename',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--filename', metavar='F', type=str, default=False,
                        help='File name', dest='filename')
    parser.add_argument('-p', '--predict', metavar='P', type=str, default=False,
                        help='Predict file name', dest='predict')
    parser.add_argument('-o', '--output', metavar='O', type=str, default=False,
                        help='Output folder name', dest='output')
    return parser.parse_args()


def writeArrayToNii(array, filename):
    itk_img = sitk.GetImageFromArray(array)
    sitk.WriteImage(itk_img, filename)


def ReadNiiToArray(filename):
    return sitk.GetArrayFromImage(sitk.ReadImage(filename))


def threshold_render(array):
    return np.where(np.logical_and(array > -950, array < -750), 1, 0)


def mergeMask(mask_A, mask_B, where_trust_B):
    return np.multiply(mask_A, np.logical_not(where_trust_B)) +\
        np.multiply(mask_B, where_trust_B)


def _test_use_threshold_render(array):
    return np.where(np.logical_and(array > -950, array < -750), 1, 0)


if __name__ == '__main__':
    args = get_args()
    image_file = args.filename
    predict_file = args.predict
    output = args.output
    img = ReadNiiToArray(image_file)
    backbone_pred = ReadNiiToArray(predict_file)

    boundary = getBoundary(backbone_pred, 3)
    writeArrayToNii(boundary, output+'boundary.nii.gz')
    PR_result = _test_use_threshold_render(img)
    writeArrayToNii(np.multiply(PR_result, boundary),
                    output+'threshold_result.nii.gz')
    result = mergeMask(backbone_pred, PR_result, boundary)
    writeArrayToNii(result, output+'result.nii.gz')
