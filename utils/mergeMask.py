import numpy as np

def onehotMaskMerge(A_pred, B_pred, where_trust_B):
    '''
        result = A if where_trust_B==0
                 B if where_trust_B==1
        AB\\where_trust_B   |0   |1
        ---------------------------
        00                  |0   |0
        01                  |0   |1
        10                  |1   |0
        11                  |1   |1
    '''
    return np.uint8(
                    (np.logical_or(np.logical_and(B_pred,where_trust_B),
                                   np.logical_and(A_pred,np.logical_not(where_trust_B)))))

def maskMerge(backbone_pred, point_rend_pred, points_to_rend):
    '''
    parameter:
        backbone_pred: a 2-D or 3-D mask 
        point_rend_pred: a 2-D or 3-D mask
        points_to_rend: an indicator shown where we trust point_rend
    return
        a tensor which is the merged mask
    '''
    # Now the label are 0,1,2...n for n+1 class, which is not good for our merge
    # We will make n+1 01 tensors for the label.
    num_classes = np.max(backbone_pred)
    onehot_merge_result = np.zeros(backbone_pred.shape)
    for cls in range(num_classes):
        temp_bkbn = np.where(backbone_pred==cls)
        temp_pr = np.where(backbone_pred==cls)
        onehot_merge_result += onehotMaskMerge(temp_bkbn,temp_pr,points_to_rend)*(cls+1)
    return onehot_merge_result