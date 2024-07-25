# Mono and Stereo Camera Calibration by Ali Parsbin
# My Website: https://parsbin.info
# My Github: https://github.com/aliparsbin
# My youtube channel: https://youtube.com/aliparsbin

import numpy as np
import cv2 as cv
import glob
import os



def mono_camera_calibration(images_path: str, patter_path: str):

    boardShape = (7,6)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objectP = np.zeros((boardShape[0] * boardShape[1], 3), np.float32)
    objectP[:,:2] = np.mgrid[0:boardShape[0], 0:boardShape[1]].T.reshape(-1,2)

    objectPoints = []
    imagePoints  = []
    
    patternFoundCounter = 0

    images = glob.glob(images_path)

    # Find chessboard pattern for each image
    for fname in images:

        # Read the image by filename
        image = cv.imread(fname)

        # Convert it to grayscale color profile
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # Finding chessboard corners from the image
        ret, corners = cv.findChessboardCorners(gray, boardShape, None)

        # If the pattern is found, then draw the chessboard corners on the image
        if ret == True:

            objectPoints.append(objectP)

            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            
            imagePoints.append(corners2)

            cv.drawChessboardCorners(image, boardShape, corners2, ret)

            cv.imshow('image', image)
            cv.imwrite(patter_path + str(patternFoundCounter) + '.jpg', image)
            patternFoundCounter += 1 
            cv.waitKey(1)


    # Camera Calibration
    retu, mtx, dist, rvecs, tvecs =  cv.calibrateCamera(objectPoints, imagePoints, gray.shape[::-1], None, None)
            
    # Error Calculation
    mean_error = 0
    for i in range(len(objectPoints)):
        imgpoints2, _ = cv.projectPoints(objectPoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imagePoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error

    mean_error /= len(objectPoints)
    cv.destroyAllWindows()
    return(mtx, mean_error)


def stereo_camera_calibration(img_1_path: str, img_2_path: str):
    
    img_1 = cv.imread(img_1_path)  #queryimage # left image
    img_2 = cv.imread(img_2_path)  #trainimage # right image
    
    img_1 = cv.cvtColor(img_1, cv.COLOR_BGR2GRAY)
    img_2 = cv.cvtColor(img_2, cv.COLOR_BGR2GRAY)

    sift = cv.SIFT_create()

    # Find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img_1,None)
    kp2, des2 = sift.detectAndCompute(img_2,None)

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

    return (F, mask)


def main():
    # cmd="mono" # or it can be "stereo"
    cmd="Stereo"
    if cmd == "mono":
        cam = 'Cam-Right' # or 'Cam-Left'
        images_path  = os.path.join('Images',cam,'RGB', '*.jpg' )
        pattern_path = os.path.join('Images',cam, 'Pattern', 'pat-')
        mtx, mean_error = mono_camera_calibration(images_path=images_path, patter_path=pattern_path)
        print(f"Intrinsic Matrix: {mtx} | Reprojection Error: {mean_error}")
    else:
        image_1_path = os.path.join('Images', 'Cam-Left', 'RGB', '01.jpg')
        image_2_path = os.path.join('Images', 'Cam-Right', 'RGB', '01.jpg')
        F, mask = stereo_camera_calibration(img_1_path=image_1_path, img_2_path=image_2_path)
        print(F)
        

if __name__ == "__main__":
    main()