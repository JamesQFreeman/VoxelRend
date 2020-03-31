import numpy as np
from scipy import misc, ndimage
from time import time

def timer(func):
    def f(*args, **kwargs):
        before = time()
        rv = func(*args, **kwargs)
        after = time()
        print("function", func.__name__,"taken",after - before)
        return rv
    return f

@timer
def _gaussian(edge,nn):
    return ndimage.gaussian_filter(edge,sigma=nn*2+1)

@timer
def _getEdge(mask):
    return ndimage.sobel(mask,1)+ndimage.sobel(mask,2)+ndimage.sobel(mask,0)

@timer
def getBoundary(mask, extend_edge = False, nn=1):
    edge = _getEdge(mask)
    if extend_edge: edge = _gaussian(edge,nn)
    binarized = (edge > 0).astype(np.int_)
    return binarized

def _testRenderForLung(voxel_value):
    

def pointRend(image, points_to_rend, render):
    '''
    parameter:
        image: a 2-D or 3-D image.
        points_to_rend: a 0/1 tensor which has the same shape as the image. 0 means dont rend; 1 means rend.
        render: a function which have a input of an image value and predict a label.
    Returns:
        a tensor which has a same shape of the input image, non-predicted area was labeled 0.
    '''
    assert image.shape == points_to_rend.shape, "image and points_to_rend should have the same shape"

    all_image_rend = render(image)
    return np.multiply(points_to_rend,all_image_rend)