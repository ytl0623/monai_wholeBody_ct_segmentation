# monai_wholeBody_ct_segmentation
You can run code with your own PC/Notebook/... or on Google Colab.
<a href="https://colab.research.google.com/github/ytl0623/monai_wholeBody_ct_segmentation/blob/master/monai_wholeBody_ct_segmentation.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

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
There are two DICOM-RT files. (Original and MONAI)

![Download DICOM directory](https://github.com/ytl0623/monai_wholeBody_ct_segmentation/assets/55120101/3a606842-88c0-4253-9072-0c5c7e2d89ee)

## Download [Dicompyler](https://github.com/bastula/dicompyler/releases/download/release-0.4.2/dicompyler_setup-0.4.2.win32.exe)
![Download Dicompyler](https://github.com/ytl0623/monai_wholeBody_ct_segmentation/assets/55120101/f39cea95-7d57-46a8-a707-db328cf8be0d)

## Show results with Dicompyler
Pay attention to the Chinese path.

![Show results with Dicompyler](https://github.com/ytl0623/monai_wholeBody_ct_segmentation/assets/55120101/9c8714fd-b28a-4493-895d-28ec621c1047)

## Reference
- https://github.com/Kiragroh/Kira_DICOM-RT-Anonymizer-MG
- https://github.com/rordenlab/dcm2niix
- https://github.com/Project-MONAI/model-zoo
- https://monai.io/model-zoo.html
