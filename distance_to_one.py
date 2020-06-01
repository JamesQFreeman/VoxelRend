import numpy as np
from time import time
from typing import List, Tuple
from utils.getBoundary import getBoundary
import SimpleITK as sitk

TEST_MATRIX = np.where((np.random.rand(500, 500, 500)) > 0.999, 1, 0)


def getDistanceToNearestOne(mat: np.ndarray) -> np.ndarray:

    pass

def _distance(p1,p2):
    return int(abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]))

def _distanceToCandidates(target: Tuple[int,int], candidates: List[Tuple[int,int]]) ->int:
    shortest_distance:int = 10000
    for candidate in candidates:
        distance = _distance(target,candidate)
        shortest_distance = min(shortest_distance,distance)
    return distance
        


def getDistanceMap2D(mat: np.ndarray) -> np.ndarray:
    (w,h) = mat.shape
    res = np.zeros((w,h))
    boundary = getBoundary(mat,3)
    boundary_points = list(zip(np.where(mat==1)))
    for i in h:
        for j in w:
            res[i,j] = _distanceToCandidates((i,j),boundary_points)

def ReadNiiToArray(filename):
    return sitk.GetArrayFromImage(sitk.ReadImage(filename))

def test():
    whole_im = ReadNiiToArray('/Users/wangsheng/Projects/UII/VoxelRend/data/case0000.nii.gz')
    im_slice = whole_im[120]
    getDistanceMap2D(im_slice)
    
test()