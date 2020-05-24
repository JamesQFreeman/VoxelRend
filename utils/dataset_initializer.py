import os
import sys
import glob
from typing import List

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

# every data can be seperated to {Image, Label, CoarseSegFloat, CoarseSegBoolean, FoldNum},
# and annoted with an id


class Data():
    def __init__(self):
        self.image = None
        self.label = None
        self.coarse_seg_float = None
        self.coarse_seg_bool = None
        self.fold_num = None

    def setImage(self, img):
        self.image = img

    def setLabel(self, label):
        self.label = label

    def setCoarseSegFloat(self, coarseSegFloat):
        self.coarse_seg_float = coarseSegFloat

    def setCoarseSegBool(self, coarse_seg_bool):
        self.coarse_seg_bool = coarse_seg_bool

    def setFoldNum(self, fold_num):
        self.fold_num = fold_num


# Dataset class should be an dict {id:Data,...}
class Dataset():
    def __init__(self, data_dir, res_dir):

        # This initializer can be divided into several parts as shown below
        # 1. Get all files' direction
        # 2. Process them to a list item for further use
        # 3. initialize the internal self.dataset

        # ------------PART 1----------------
        # first * for the fold num
        # second * for the id
        img_list = glob.glob(data_dir+'/*/*/thin.nii.gz')
        label_list = glob.glob(data_dir+'/*/*/2019_ncov_final.nii.gz')

        # * for the id
        seg_f_list = glob.glob(res_dir+'/*/prob_2.mhd')
        seg_b_list = glob.glob(res_dir+'/*/seg.nii.gz')

        # -------------PART 2-------------
        # id = img_dir.split('/')[-2]
        # fold_num = img_dir.split('/')[-3]
        # img_dir = img_dir
        # same thing for the label
        img_list = [[img_dir.split('/')[-2], img_dir.split('/')[-3], img_dir]
                    for img_dir in img_list]
        label_list = [[label_dir.split('/')[-2], label_dir.split('/')[-3], label_dir]
                      for label_dir in label_list]

        seg_f_list = [[seg_f_dir.split('/')[-2], seg_f_dir]
                      for seg_f_dir in seg_f_list]
        seg_b_list = [[seg_b_dir.split('/')[-2], seg_b_dir]
                      for seg_b_dir in seg_b_list]

        # this is for debug use
        # print('img_list_content:', img_list[:3])
        # print('label_list_content:', label_list[:3])
        # print('seg_f_list_content:', seg_f_list[:3])
        # print('seg_b_list_content:', seg_b_list[:3])

        # ------------PART 3------------

        # Now we should get all the id and initialize Data object for them
        self.dataset = {}
        id_list = [x[0] for x in img_list]
        for _id in id_list:
            self.dataset[_id] = Data()

        # Now we set them
        for item in img_list:
            _id, fold_num, img_dir = item
            self.dataset[_id].setImage(img_dir)
            self.dataset[_id].setFoldNum(fold_num)

        for item in label_list:
            _id, _, label_dir = item
            self.dataset[_id].setLabel(label_dir)

        for item in seg_f_list:
            _id, seg_f_dir = item
            self.dataset[_id].setCoarseSegFloat(seg_f_dir)

        for item in seg_b_list:
            _id, seg_b_dir = item
            self.dataset[_id].setCoarseSegBool(seg_b_dir)

        print('A VoxelRend Dataset have been initialized from {} and {}'\
            .format(data_dir, res_dir))
        print('Consist of {} cases in total.'.format(len(img_list)))
        print('{} of them have coarse segmentation'.format(len(seg_b_list)))

    def _splitLastThreeDir(self, d: str) -> List[str]:
        # get some dir and return the last three dir/file
        l = d.split('/')
        return [l[-3], l[-2], l[-1]]

    def getImage(self, _id):
        return img

    def getLabel(self, _id):
        pass

    def getSegPossibility(self, _id):
        pass

    def getSeg(slef, _id):
        pass


Dataset(ORIGINAL_DATA_DIR, COARSE_DIRECTION_RESULT_DIR)
