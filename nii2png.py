import os
import nibabel as nib
import numpy as np
import cv2
import glob
from natsort import natsorted
from organList import *

def _one_hot_encoder(input_data):
    label_list = [[] for i in range(n_classes)]
    for i in range(n_classes):
        temp_prob = input_data == i  ##取出第幾類
        temp_prob = np.squeeze(temp_prob)
        label_list[i].append(temp_prob)
        # print(np.unique(label_list[i]))  ##True/False的masks
        label_list[i] = np.squeeze(np.array(label_list[i]))*255 ##為了存成uint8來可視化,所以*255
        # print(np.unique(label_list[i])) 
    output_tensor = np.array(label_list)
    return output_tensor


NIFTI_data = 'NIFTI/'
DCM_data = 'DICOM/'
output_dir = 'MONAI/'
n_classes = len(Organ)

list_patient = os.listdir(NIFTI_data)
list_patient = natsorted(list_patient)

for patient_path in list_patient:
    print(patient_path, '='*50)
    patient_path = patient_path + '/'
    NIFTI_Folder = NIFTI_data + patient_path
    DCM_Folders = DCM_data + patient_path
    list_nii= glob.glob(NIFTI_Folder + '*_trans.nii')
    list_CT= glob.glob(DCM_Folders + 'CT*.dcm')
    list_nii= natsorted(list_nii, reverse=False)
    list_CT= natsorted(list_CT, reverse=False)

    label_Sequence = []
    for niiFileName in list_nii:
        print('Reading:', niiFileName)
        nii = nib.load(niiFileName)
        label_part = nii.get_fdata()
        # affine===================================
        if nii.affine[0, 0] > 0:
            label_part = np.flip(label_part, axis=0)
        if nii.affine[1, 1] > 0:
            label_part = np.flip(label_part, axis=1)
        if nii.affine[2, 2] > 0:
            label_part = np.flip(label_part, axis=2)
        # ==========================================
        label_part = np.transpose(label_part, (2,1,0))
        label_Sequence += list(label_part)
    label_Sequence = np.array(label_Sequence)
    label_Sequence = _one_hot_encoder(label_Sequence)
    print('Label\'s shape:\n', label_Sequence.shape)

    for i, organ_name in enumerate(Organ):
        dir_path = output_dir + patient_path + 'MONAI_' + organ_name + '/'
        # print('Output:', dir_path)
        if(label_Sequence[i].any()>0):
            if os.path.exists(dir_path)==False:
                os.makedirs(dir_path)
            for j in range(len(label_Sequence[i])):
                path = list_CT[j].replace(DCM_data, output_dir)
                path = path.replace('\\', '/')
                path = path.replace(patient_path, patient_path + 'MONAI_' + organ_name + '/')
                path = path.replace('.dcm', '_OUT.png')
                cv2.imwrite(path, label_Sequence[i][j])
