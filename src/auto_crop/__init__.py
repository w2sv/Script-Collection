import os
from itertools import starmap

import cv2
import numpy as np


croppingDir = 'C:/Users/User/Pictures/testScreens'
destDir = 'C:/Users/User/Pictures/croppedScreenshotsTest'

# creating saving destination dir if necessary
latestFileInd = 0
if not os.path.isdir(destDir):
	os.makedirs(destDir)
# if already existent retrieve latest cropImgInd
else:
	if len(os.listdir(destDir))
		filenames = [file[:file.rfind('.')] for file in os.listdir(destDir)]
		latestFileInd = int(sorted(filenames)[-1][-1]) + 1

oldDirSize = len(os.listdir(destDir))

# iterating through files
stdThresh = 1
for fileInd, file in enumerate(os.listdir(croppingDir)):
	imgLink = os.path.join(croppingDir, file)
	arr = cv2.imread(imgLink)

	sliceInds = [] 
	currIndList = []

	if not fileInd % 10:
		print("current img ind: ", fileInd)
	
	for rowInd, row in enumerate(arr[:-1]):
		if not len(currIndList):
			if np.std(row) < stdThresh and np.std(arr[rowInd+1]):
				currIndList.append(rowInd)
		else:
			if np.std(row) and np.std(arr[rowInd+1]) < stdThresh or rowInd+1 == len(arr)-1:
				currIndList.append(rowInd)
				sliceInds.append(tuple(currIndList))
				currIndList = []
	
	sliceHeightList = list(starmap(lambda a,b: np.abs(a-b),sliceInds))
	maxHeightInd = np.argmax(sliceHeightList)
	maxGapTuple = sliceInds[maxHeightInd]

	# save cropped image if surpassing 1/4 of original image height
	if sliceHeightList[maxHeightInd] > (len(arr) / 4.0):
		croppedImg = arr[maxGapTuple[0]+1:maxGapTuple[1]]
		cv2.imwrite(os.path.join(destDir,f'cropped{latestFileInd}.png'),croppedImg)
		latestFileInd += 1

print(f"cropped {len(os.listdir(destDir))-oldDirSize} out of {len(os.listdir(croppingDir))} images")