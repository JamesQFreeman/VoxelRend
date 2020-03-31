# VoxelRend
 A modified pointrend for 3D medical image 

## File description

```bash
Med-PointRend/
    data/
        images/
            case_0001.nii.gz
            ...
        labels/
            case_0001.nii.gz
            ...
        preds/
            case_0001.nii.gz
            ...
    utils/
        getBoundary.py
        mergeMask.py
        dataset.py
    tools/
        train.py
        inference.py
        preprocess.py
    models/
        MLP.py
    checkpoints/
        2020-04-01-20-30.checkpoint
        ...
    results/
```

## Train

```bash
python.py tools/train.py
```

## Inference

```bash
python.py tools/inference.py checkpoints/2020-04-01-20-30.checkpoint --out==results/test1/
```