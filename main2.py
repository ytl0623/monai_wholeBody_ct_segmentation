from SegmentiontoImageData import SegmentiontoImageData
from ImagetoRT import *
import os
import datetime
import glob
import time
from organList import *  # "Organ" and "color_table"

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

if __name__ == "__main__":
    start = time.time()

    NIFTI_data = 'NIFTI/'
    DCM_data = 'DICOM/'
    output_dir = 'MONAI/'
    n_classes = len(Organ)

    list_patient = os.listdir(NIFTI_data)
    list_patient = natsorted(list_patient)

    for patient_path in list_patient:
        print(patient_path, '=' * 50)
        patient_path = patient_path + '/'
        NIFTI_Folder = NIFTI_data + patient_path
        DCM_Folders = DCM_data + patient_path
        list_nii = glob.glob(NIFTI_Folder + '*_trans.nii')
        list_CT = glob.glob(DCM_Folders + 'CT*.dcm')
        list_nii = natsorted(list_nii, reverse=False)
        list_CT = natsorted(list_CT, reverse=False)

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
            label_part = np.transpose(label_part, (2, 1, 0))
            label_Sequence += list(label_part)
        label_Sequence = np.array(label_Sequence)
        label_Sequence = _one_hot_encoder(label_Sequence)
        print('Label\'s shape:\n', label_Sequence.shape)

        for i, organ_name in enumerate(Organ):
            dir_path = output_dir + patient_path + 'MONAI_' + organ_name + '/'
            # print('Output:', dir_path)
            if (label_Sequence[i].any() > 0):
                if os.path.exists(dir_path) == False:
                    os.makedirs(dir_path)
                for j in range(len(label_Sequence[i])):
                    path = list_CT[j].replace(DCM_data, output_dir)
                    path = path.replace('\\', '/')
                    path = path.replace(patient_path, patient_path + 'MONAI_' + organ_name + '/')
                    path = path.replace('.dcm', '_OUT.png')
                    cv2.imwrite(path, label_Sequence[i][j])


    dataset_folders = 'MONAI/'
    patient_folders = os.listdir(dataset_folders)

    for patient_folder in patient_folders:
        print(patient_folder, '=' * 50)
        label_path = 'MONAI/' + patient_folder + '/'
        dcm_file_path = 'DICOM/' + patient_folder + '/'

        print(dcm_file_path, label_path)

        spacingDatabase, DICOMInformation = SegmentiontoImageData(dcm_file_path, label_path)()

        try:
            RT_filename = glob.glob(dcm_file_path + 'RS*.dcm')[0]
        except:
            RT_filename = glob.glob(dcm_file_path + 'RTSTRUCT_*.dcm')[0]

        print(RT_filename)

        DICOM_RT = pydicom.dcmread(RT_filename)
        # DICOM_RT = pydicom.dcmread(dcm_file_path + 'AI_2.16.840.1.113669.2.931128.13525386.20221107152223.918302.dcm')
        # print(DICOM_RT)

        AI_DICOM_RT = ImagetoRT(spacingDatabase, DICOMInformation, DICOM_RT, Organ)()

        # 特殊格式
        ISOTIMEFORMAT = '%Y%m%d'
        date = datetime.date.today().strftime(ISOTIMEFORMAT)
        AI_DICOM_RT.StructureSetLabel = 'MONAI_Pred' + date
        AI_DICOM_RT.file_meta.MediaStorageSOPInstanceUID = DICOM_RT.SOPInstanceUID + date
        # '1.2.246.352.71.4.753219990087.110632.2017032321550020201013.dcm'
        AI_DICOM_RT.SOPInstanceUID = DICOM_RT.SOPInstanceUID + date
        # AI_DICOM_RT.file_meta.ImplementationClassUID = '1.3.6.1.4.1.9590.100.1.3.100.9.4'
        # pydicom.dataset.validate_file_meta(AI_DICOM_RT.file_meta)
        RT_filename = RT_filename.replace('RS', 'RS_MONAI')
        # RT_filename = RT_filename.replace('RTSTRUCT','AI_RTSTRUCT')
        pydicom.filewriter.dcmwrite(RT_filename, AI_DICOM_RT, write_like_original=True)

        # AI_DICOM_RT.save_as('python_cust_uid.dcm')
        end = time.time()
        print("執行時間：%f 秒\n\n" % (end - start))