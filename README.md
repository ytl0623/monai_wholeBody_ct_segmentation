# monai_wholeBody_ct_segmentation

## Create a virtual environment
```
conda create -n [NAME] python==3.9
```

## Start the environment
```
conda activate [NAME]
```

## Clone Repository
```
git clone https://github.com/ytl0623/monai_wholeBody_ct_segmentation.git
```

## Go to the cloned folder
```
cd monai_wholeBody_ct_segmentation
```

## Install the dependencies
```
pip install -r requirements.txt
```

## Setting the directory
```
cd models/wholeBody_ct_segmentation/
```

## Execute inference
It will cost about three minutes.
Check NIFTI directory after run done.
```
python -m monai.bundle run --config_file configs/inference.json
```

## Unzip inference file
```
gzip -d NIFTI/DLCSI033/DLCSI033_trans.nii.gz 
```

## Convert NIFTI file to mask file
It will cost about three minutes.
Check MONAI directory after run done.
```
python nii2png.py
```

## Generate DICOM-RT file
It will cost about two minutes.
Check DICOM directory after run done.
```
python main.py
```

## Download DICOM directory

## Download [Dicompyler](https://github.com/bastula/dicompyler/releases/download/release-0.4.2/dicompyler_setup-0.4.2.win32.exe)
![螢幕擷取畫面 2023-08-07 162717](https://github.com/ytl0623/monai_wholeBody_ct_segmentation/assets/55120101/f39cea95-7d57-46a8-a707-db328cf8be0d)

## Show results with Dicompyler
Pay attention to the Chinese path.
![螢幕擷取畫面 2023-08-07 162941](https://github.com/ytl0623/monai_wholeBody_ct_segmentation/assets/55120101/9c8714fd-b28a-4493-895d-28ec621c1047)

## Reference
- https://github.com/Project-MONAI/model-zoo
- https://monai.io/model-zoo.html
