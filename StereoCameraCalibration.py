# AMR-Robot Stereo Camera Calibration  by Ali Parsbin
# Checkout youtube.com/aliparsbin

import numpy as np
import cv2 as cv
import os


img1 = cv.imread(os.path.join(os.path.dirname(__file__), 'Images\Cam-Left\Gray' , 'pat-0.jpg'), 0)  #queryimage # left image
img2 = cv.imread(os.path.join(os.path.dirname(__file__), 'Images\Cam-Right\Gray', 'pat-0.jpg'), 0) #trainimage # right image

sift = cv.SIFT_create()

# Find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)

pts1 = []
pts2 = []

# Ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.8*n.distance:
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
F, mask = cv.findFundamentalMat(pts1,pts2,cv.FM_LMEDS)

print(F)