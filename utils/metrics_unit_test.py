from metrics import *
import SimpleITK as sitk
from voxelrender_dataset import Dataset

# this direction store the results
# result
#       id
#           prob_2.mhd // This is the prob
#           seg.nii.gz // Seg
COARSE_DIRECTION_RESULT_DIR = '/data1/shengwang/result'


# The data consist of several fold
# which should be
# covid
#       2019-nCov1
#           id
#               thin.nii.gz // this is the image
#               2019_ncov_final.nii.gz // this is the label
#           ...
#       2019-nCov2
#           ...
ORIGINAL_DATA_DIR = '/home/shengwang/covid'

vr_ds = Dataset(ORIGINAL_DATA_DIR, COARSE_DIRECTION_RESULT_DIR)


def ReadNiiToArray(filename):
    return sitk.GetArrayFromImage(sitk.ReadImage(filename))


def unitTestDiceCoef():
    five_cases = vr_ds.getCoarseSegIdList()[:5]
    for pid in five_cases:
        print('Patient ID: {}'.format(pid))
        label = ReadNiiToArray(vr_ds.getLabel(pid))
        pred = ReadNiiToArray(vr_ds.getSeg(pid))
        print('The shape of label and pred are: {} and {}'.format(
            label.shape, pred.shape))
        print('The dice coef of each class is: {}'.format(diceCoef(label, pred)))
        print('The avg dice is: {}'.format(averageDiceCoef(label, pred)))


unitTestDiceCoef()
