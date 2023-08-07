from SegmentiontoImageData import SegmentiontoImageData
from ImagetoRT import *
import os 
import datetime
import glob
import time
from organList import *   # "Organ" and "color_table"

if __name__ == "__main__":
    start = time.time()

    dataset_folders = 'MONAI/'
    patient_folders = os.listdir(dataset_folders)
    
    for patient_folder in patient_folders:
        print(patient_folder, '='*50)
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
        date=datetime.date.today().strftime(ISOTIMEFORMAT)
        AI_DICOM_RT.StructureSetLabel = 'MONAI_Pred' + date
        AI_DICOM_RT.file_meta.MediaStorageSOPInstanceUID = DICOM_RT.SOPInstanceUID + date
        #'1.2.246.352.71.4.753219990087.110632.2017032321550020201013.dcm'
        AI_DICOM_RT.SOPInstanceUID = DICOM_RT.SOPInstanceUID + date
        # AI_DICOM_RT.file_meta.ImplementationClassUID = '1.3.6.1.4.1.9590.100.1.3.100.9.4'
        # pydicom.dataset.validate_file_meta(AI_DICOM_RT.file_meta)
        RT_filename = RT_filename.replace('RS','RS_MONAI')
        # RT_filename = RT_filename.replace('RTSTRUCT','AI_RTSTRUCT')
        pydicom.filewriter.dcmwrite(RT_filename, AI_DICOM_RT, write_like_original=True)

        # AI_DICOM_RT.save_as('python_cust_uid.dcm')
        end = time.time()
        print("執行時間：%f 秒\n\n" % (end - start))