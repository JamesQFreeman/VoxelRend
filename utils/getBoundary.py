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
    '''
    parameter:
        mask: 2d or 3d array
        extend_edge: bool, if True then the edge will be extend
        nn: int, how much the edge line will be extend when the extend_edge is True
    return:
        array, which have the same size as the mask, and edge voxels are labeled as 1 while rest are 0
    '''
    edge = _getEdge(mask)
    if extend_edge: edge = _gaussian(edge,nn)
    binarized_boundary = (edge > 0).astype(np.int_)
    return binarized_boundary