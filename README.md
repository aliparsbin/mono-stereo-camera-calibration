# Camera Calibration

The aim of the camera calibration is to find the **Intrinsic and Extrinsic Parameters** for the camera to remove the *distortion* in images. 

## Mono Camera Calibration

1. Extrinsic Parameters: corresponds to rotation and translation vectors which translate the coordinates of a 3D point to a coordinate system.
2. Intrinsic Parameters: they include information like focal length `(fx, fy)` and optical centers `(cx, cy)`.
   The focal length and optical centers can be used to create a camera matrix, which can be used to remove distortion due to the lenses of a specific camera.
   The camera matrix is unique to a specific camera, so once calculated, it can be reused on other images taken by the same camera. It is expressed as a 3x3 matrix:

   ![image](https://github.com/user-attachments/assets/0e16431f-eb2a-4f8a-a914-9bf92bf7c974)

How to experiment: We find some specific points of which we already know the relative positions (e.g., square corners in the chess board). 
We know the coordinates of these points in real-world space, and we know the coordinates in the image, so we can solve for the distortion coefficients. 
For better results, we need at least `10` test patterns.

The method `mono_camera_calibration()` is written for the mono camera calibration, which takes `images_path` and `patterns_path` and returns the camera matrix, distortion coefficients,
rotation, translation vectors, and mean_error while saving the pattern images in the specified location.

### Result

Input image captured by the camera:

![IMG_20210610_160728](https://github.com/user-attachments/assets/33127a83-51e3-48d0-92c8-ea5969f96e24)


Output image (found chessboard pattern): 

![pat-6](https://github.com/user-attachments/assets/f94572ea-dede-476f-a21d-aa898500ba18)


## Stereo Camera Calibration

The stereo camera consists of two cameras placed at a distance. As we do not have a stereo camera, we used two mono cameras for this experiment.

The aim is to find the intrinsic parameters of cameras and extrinsic parameters of the stereo (rotation and translation vector of the right camera corresponding to the left camera). In the stereo camera, the left camera is our origin.

![image](https://github.com/user-attachments/assets/75636dce-bcf5-4516-9e2d-7fe59109886b)

The method `stereo_camera_calibration()` is written for the mono camera calibration, which takes `image1_path` and `image2_path` and returns the fundamental matrix, including the rotation and translation vectors.
