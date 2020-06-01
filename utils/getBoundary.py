import numpy as np
from scipy import misc, ndimage
from time import time
import torch


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
def torchGetBoundary2D(mask, boundary_width):
    max_pool = torch.nn.MaxPool2d(boundary_width, 1)
    avg_pool = torch.nn.AvgPool2d(boundary_width, 1)
    return max_pool(mask) - avg_pool(mask)


@timer
def getBoundary(mask, boundary_width):
    assert boundary_width % 2 == 1, "Boundary width should be odd number, now getting {}".format(
        boundary_width)
    dim = mask.ndim
    mask = np.pad(mask, (boundary_width)//2)
    mask = torch.unsqueeze(torch.from_numpy(mask), 0)
    if dim == 3:
        edge = torchGetBoundary(mask, boundary_width)
    if dim == 2:
        edge = torchGetBoundary2D(mask, boundary_width)
    binarized = torch.squeeze((edge > 0))
    return binarized.numpy().astype(np.int_)
