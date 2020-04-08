import argparse
import os
import sys

import numpy as np
import torch
import torch.nn as nn
from torch import optim

from models.MLP import MLP

from utils.dataset import BasicDataset
from torch.utils.data import DataLoader, random_split

dir_img = "data/images/"
dir_mask = "data/labels/"
dir_checkpoints = "checkpoints/"


def inference(mode,
              weight_file,
              output_dir
              ):
    
    if mode == 'threshold':
        threshold_inference(output_dir)
    elif mode == 'MLP':
        pass
    else:
        raise ValueError("only support threshold and MLP for now")
    pass
    
def get_args():
    parser = argparse.ArgumentParser(description='Train the PointRender on images and pre-processed labels',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-m', '--mode', metavar='M', type=str, nargs='?', default='threshold',
                        help='Mode', dest='mode')
    parser.add_argument('-f', '--load', dest='load', type=str, default=False,
                        help='Load model from a .pth file')
    parser.add_argument('-o', '--output-dir', dest='outputdir', type=str, default='results/',
                        help='The output path')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    #device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    #net = MLP(1,3)

    #if args.load:
    #    net.lead_state_dict(
    #        torch.load(args.load, map_location=device)
    #    )

    #net.to(device=device)

    try:
        inference(args.mode, args.weight_file, args.output_dir)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
