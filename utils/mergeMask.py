import numpy as np


def mergeMask(mask_A, mask_B, where_trust_B):
    return np.multiply(mask_A, np.logical_not(where_trust_B)) +\
        np.multiply(mask_B, where_trust_B)
