import numpy as np
from scipy import misc, ndimage
from time import time
import torch
import argparse
import SimpleITK as sitk


def testVoxelRender(patch):
    # Input a 9x9x9 output a 1x1x1
    m = np.mean(patch)
    return (m>750).astype(np.int_)


def binarize(img):
    return (img > 0.5).astype(np.int_)

def getCenter(img):
    pass

def voxelRendProcess(img, voxelrender):
    # input size (x,y) output size (x//9, y//9)
    # We just cut out the edge
    (w,h) = img.shape
    w%9
    vvr = np.vectorize(voxelrender)
    img = vvr(img)
    return img


def mainProcess(img):
    # Let's assume it's 512x512
    # Then there should be 3 voxelrender,
    # take a 36x36x36 patch in, give out a 4x4x4 result(all 64 ele should be the same)
    # take a 18x18x18 patch->2x2x2 result(all 8 ele should be the same)
    # take a 9x9x9 patch->2x2x2 result(all 8 ele should be the same)

    # First, the confidence output of the coarse seg(0-1) give the weight.
    coarse_weight = unet_wo_softmax(img)
    coarse_res = binarize(coarse_weight)

    # vr for VoxelRender
    scale1_img = resizeImg(img, 128)
    sacle1_res = voxelRendProcess(scale1_img, vr1)
    scale2_img = resizeImg(img, 256)
    sacle2_res = voxelRendProcess(scale2_img, vr2)
    scale3_img = img.copy()
    sacle3_res = voxelRendProcess(scale3_img, vr3)

    result = coarse_weight * coarse_res + \
        (1/3)*(1-coarse_weight)*(sacle1_res+scale2_res+scale3_res)

    return binarize(result)

# This should be a


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
