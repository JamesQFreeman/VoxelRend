import numpy as np


def diceCoef(label, pred, smooth=1):
    num_class = max(np.max(label), np.max(pred))+1
    dice_coef_class_list = []
    for c in range(int(num_class)):
        single_class_label = np.where(label == c, 1, 0)
        single_class_pred = np.where(pred == c, 1, 0)
        dice_coef = singleDiceCoef(
            single_class_label, single_class_pred, smooth)
        dice_coef_class_list.append(dice_coef)
    return dice_coef_class_list


def averageDiceCoef(label, pred, smooth=1):
    return np.mean(diceCoef(label, pred, smooth))


def singleDiceCoef(y_true, y_pred, smooth=1):
    intersection = np.sum(np.multiply(y_true, y_pred))
    union = np.sum(y_true) + np.sum(y_pred)
    dice = (2. * intersection + smooth)/(union + smooth)
    return dice
