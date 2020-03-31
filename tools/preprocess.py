from utils import getBoundary
import glob.glob
import numpy as np

def _single_case(image, mask, density=0.1):
    boundary = getBoundary(mask)
    one_voxels = np.where(boundary==1)
    boundary_voxel_index_list = list(zip(one_voxels[0],one_voxels[1],one_voxels[2]))
    num_points = len(boundary_voxel_index_list)

    single_image_res = np.zeros((2,num_points))
    for i in range(num_points):
        x,y,z = boundary_voxel_index_list[i]
        X = image[x,y,z]
        Y = mask[x,y,z]
        single_image_res[i,0] = X
        single_image_res[i,1] = Y
    
    return single_image_res

def preprocess(density=0.1, output="./data/points_train/points.npy"):
    '''
    parameter:
        density: how much voxel you want remove during the training, 1.0 means no remove, which is the same as the inference 

    Store the preprocess data in the ./data/points_train/points.npy
    '''
    dir_img = "./data/images/"
    dir_mask = "./data/labels"

    print("We got {} cases".format(num_cases))
    # assume we got all the results
    res_list = []
    res = np.concatenate(res_list, axis=1)
    num_points = len(res[0])
    print("We processed {} points".format(num_points))
    np.save(output,res)
    
    

def get_args():
    parser = argparse.ArgumentParser(description='Pre-process to prepare the dataset for the pointrender to train',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--point-density', metavar='D', type=float, nargs='?', default=0.1,
                        help='Point Density', dest='pointdensity')
    parser.add_argument('-o', '--output', metavar='O', type=str, nargs='?', default="./data/points_train/points.npy",
                        help='Output', dest='o')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    
    net.to(device=device)

    try:
        train_net(net=net,
                  epochs=args.epochs,
                  batch_size=args.batchsize,
                  lr=args.lr,
                  device=device,
                  val_percent=args.val / 100)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
