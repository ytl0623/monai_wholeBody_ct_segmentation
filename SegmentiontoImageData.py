import numpy as np
import pydicom
import os
import re
import cv2
from natsort import natsorted
import matplotlib.pyplot as plt

class SegmentiontoImageData():
	def __init__(self, DICOM_File, predict_File):
		self.pixelSpacing = (1,1)
		self.initial_position = (1,1,1)
		self.DICOM_File_PATH = DICOM_File

		self.predict_File_PATH = predict_File
	#	self.itemColorList_txt = itemColorList_txt
		self.pixelDatabase = []
		# self.items = []
		self.itemsLen = 0
	#	self.ROIColor = []
		self.DICOMInformation = []
		self.spacingDatabase = []
		self.contourSequence = []
		self.imageList = []
		self.numberOfImage = 0
		
	def __call__(self):
		print('get Contour Sequence from Images.', end='')  #從影像獲取輪廓
		self.getDICOMinformation()
	#	self.getItemColor()
		self.getImageData()
		self.pixeltoSpacing()
		return [self.spacingDatabase, self.DICOMInformation]
	
	def getSliceLocation(self, filename):
		for i in range(len(self.DICOMInformation)):
			# if(self.DICOMInformation[i].SOPInstanceUID == filename):
			if(self.DICOMInformation[i].SOPInstanceUID == filename[3:]):
				return self.DICOMInformation[i].SliceLocation
		return -1
		
	def getDICOMinformation(self):
		DICOMdir = os.listdir(self.DICOM_File_PATH)
		# DICOMdir.sort()
		DICOMdir = natsorted(DICOMdir)
		# print(DICOMdir)			

		for DICOMName in DICOMdir:
			filename = self.DICOM_File_PATH + DICOMName
			# print(filename)
			dataset = pydicom.dcmread(filename)
			if(dataset.Modality == "CT"):
				self.DICOMInformation.append(dataset)
		self.pixelSpacing = self.DICOMInformation[0].PixelSpacing
		self.initial_position = self.DICOMInformation[0].ImagePositionPatient

	# def getItemColor(self):
	# 	with open(self.itemColorList_txt) as f:
	# 		content = f.read()
	# 	x = re.split(",|:|\[|\]|\*|\n|'",str(content))
	# 	for i in range(0, len(x)-1, 6):
	# 		item = x[i]
	# 		R = int(x[i+2].split('\"')[1])
	# 		G = int(x[i+3].split('\"')[1])
	# 		B = int(x[i+4].split('\"')[1])
	# 		self.items.append(item)
	# 		self.ROIColor.append([item, [B, G, R]])

	# def getItemColor(self):
	# 	with open(self.itemColorList_txt) as f:
	# 		content = f.read()

	# 	x = re.split(",|:|\[|\]|\*|\n|'",str(content))
	# 	separation_count = x.count("==========================================")

	# 	if separation_count :
	# 		separation_index = x.index("==========================================")
	# 		x = x[:separation_index]

	# 	for i in range(0, len(x)-1, 8):
	# 		item = x[i]
	# 		R = int(x[i+2].split('\"')[1])
	# 		G = int(x[i+3].split('\"')[1])
	# 		B = int(x[i+4].split('\"')[1])
	# 		self.items.append(item)
	# 		self.ROIColor.append([item, [B, G, R]])

			
	def getImageData(self):
		itemsdir = os.listdir(self.predict_File_PATH)
		# itemsdir.sort()
		itemsdir = natsorted(itemsdir)
		# print("----------------------")
		# print(itemsdir)
		# print("----------------------")
		self.itemsLen = len(itemsdir)
		for item in itemsdir:
			path = self.predict_File_PATH + item
			imagesdir = os.listdir(path)
			# imagesdir.sort()
			imagesdir = natsorted(imagesdir)
			# print(len(imagesdir))
			self.numberOfImage = len(imagesdir)
			pixelData = []
			z_axis = -1
			for imageName in imagesdir:
				name = imageName[:-4]
				# name = 'CT.'+imageName[:-4]
				# name = imageName[3:-4]
				name = name.replace('_OUT', '')
				image = cv2.imread(path + "/" + imageName)       # 這邊是一張一張讀進來，若是nifti格式可以一次讀再進到這個for迴圈
				imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				ret,thresh = cv2.threshold(imgray,127,255,0)

				#plt.imshow(thresh)
				#plt.show()

				#map = np.zeros((512, 512, 3))
				contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

				z_axis = z_axis + 1
				if(contours == []):
					continue
				temp = []
				for cnt in contours:
					cnt = list(np.array(cnt).reshape(-1))
					temp.append(cnt)

				pixelData.append([name, temp])

				#for cnt in contours:
					#pixelData.append(cnt)
					#cv2.drawContours(map, cnt, -1, (0, 255, 0), -1)
					#cv2.imshow("test",map)
					#cv2.waitKey(30)
			#print(item)
			#print(len(pixelData))

			self.pixelDatabase.append([item ,pixelData])


			
	def pixeltoSpacing(self):

		# organs
		for itemNumber in range(self.itemsLen):
			item, itemData = self.pixelDatabase[itemNumber]
			# print(itemData)
			database = []
			# organ's images
			for imageNumber in range(len(itemData)):
				contours = []
				name, contoursData = itemData[imageNumber]
				z_axis = self.getSliceLocation(name)
				# image's contour
				for numberOfContour in range(len(contoursData)):
					coordinate = []
					pixelData = contoursData[numberOfContour]
					# contour to real world coordinate
					for i in range(0, len(pixelData), 2):
						x = pixelData[i]
						y = pixelData[i+1]
						xx = x * self.pixelSpacing[0] + self.initial_position[0] 
						yy = y * self.pixelSpacing[1] + self.initial_position[1] 
						zz = z_axis
						coordinate.append([xx, yy, zz])
						# print(coordinate)
					contours.append(coordinate)
				if item=='AIBODY':
					if len(contours)>1:
						for i in contours:
							if len(i)>300:
								BODY_filter = [i]
						contours = BODY_filter
					# with open('neckBody.txt', 'a') as f:
					# 	for point in contours[0]:
					# 		print(point, file=f)

				database.append(contours)
			self.spacingDatabase.append([item, database])

		# print(len(self.spacingDatabase))   # 將label以點的形式寫入