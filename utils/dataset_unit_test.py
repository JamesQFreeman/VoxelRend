from voxelrender_dataset import Dataset
import SimpleITK as sitk
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
print('\n\nIn this unit test we confirm the all the id are correct')
pid_list = vr_ds.getIdList()
ds_size = len(pid_list)
for pid in range(ds_size//10):
    print(pid_list[pid*10])

# In this unit test we confirm the all the getFoldNum() are working correctly
print('\n\nIn this unit test we confirm the all the getFoldNum() are working correctly')
pid_list = vr_ds.getIdList()
ds_size = len(pid_list)
for pid in range(ds_size//10):
    _pid = pid_list[pid*10]
    print('from {} we got {}'.format(vr_ds.getFoldNum(_pid), _pid))


def writeArrayToNii(array, filename):
    itk_img = sitk.GetImageFromArray(array)
    sitk.WriteImage(itk_img, filename)


def ReadNiiToArray(filename):
    return sitk.GetArrayFromImage(sitk.ReadImage(filename))


# In this unit test we confirm the all the getImage() are working correctly
print('\n\nIn this unit test we confirm the all the getImage() are working correctly')
pid_list = vr_ds.getIdList()
ds_size = len(pid_list)
for pid in range(ds_size//10):
    _pid = pid_list[pid*100]
    im_array = ReadNiiToArray(vr_ds.getImage(_pid))
    print('Image shape: {} from {}'.format(im_array.shape(), _pid))

# In this unit test we confirm the all the getLabel() are working correctly
print('\n\nIn this unit test we confirm the all the getLabel() are working correctly')
pid_list = vr_ds.getIdList()
ds_size = len(pid_list)
for pid in range(ds_size//10):
    _pid = pid_list[pid*100]
    im_array = ReadNiiToArray(vr_ds.getLabel(_pid))
    print('Image shape: {} from {}'.format(im_array.shape(), _pid))


# In this unit test we confirm the all the getSegPossibility() are working correctly
print('\n\nIn this unit test we confirm the all the getSegPossibility() are working correctly')
pid_list = vr_ds.getIdList()
ds_size = len(pid_list)
for pid in range(ds_size//10):
    _pid = pid_list[pid*100]
    im_array = ReadNiiToArray(vr_ds.getSegPossibility(_pid))
    print('Image shape: {} from {}'.format(im_array.shape(), _pid))


# In this unit test we confirm the all the getSeg() are working correctly
print('\n\nIn this unit test we confirm the all the getSeg() are working correctly')
pid_list = vr_ds.getIdList()
ds_size = len(pid_list)
for pid in range(ds_size//10):
    _pid = pid_list[pid*100]
    im_array = ReadNiiToArray(vr_ds.getSeg(_pid))
    print('Image shape: {} from {}'.format(im_array.shape(), _pid))

