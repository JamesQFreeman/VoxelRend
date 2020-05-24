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

# patient ID is annoted as pid
# In this unit test we confirm the all the id are correct
pid_list = vr_ds.getIdList()
ds_size = len(pid_list)
for pid in range(ds_size//10):
    print(pid_list[pid*10])