import numpy as np

def _stat(array1d):
    result = {}
    result['Voxel number'] = len(array1d)
    result['Mean Value'] = np.mean(array1d)
    result['Std'] = np.std(array1d)
    result['Max'] = np.max(array1d)
    result['Min'] = np.min(array1d)
    result['95% max'] = np.percentile(array1d,95)
    result['95% min'] = np.percentile(array1d,5)
    return result

def localStat(target_area, target):
    filtered = np.multiply(target_area, target) # use target area as a filter
    # The problem is we can't analyse zero in the target, never mind that. FUCK THAT
    flattened = filtered.flatten().trim_zeros() # flatten to 1d array and remove all the zeros
    return _stat(flattened)

def misLabelStat(pred, true, img):
    mis_label = np.logical_xor(pred,true)
    localStat(mis_label, img)
