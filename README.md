# Mono Camera Calibration

The aim of the camera calibration is to find the **Intrinsic and Extrinsic Parameters** for the camera to remove the *distortion* in images. 

1. Extrinsic Parameters: corresponds to rotation and translation vectors which translate the coordinates of a 3D point to a coordinate system.
2. Intrinsic Parameters: They include information like focal length `(fx, fy)` and optical centers `(cx, cy)`.
   The focal length and optical centers can be used to create a camera matrix, which can be used to remove distortion due to the lenses of a specific camera.
   The camera matrix is unique to a specific camera, so once calculated, it can be reused on other images taken by the same camera. It is expressed as a 3x3 matrix:

   ![image](https://github.com/user-attachments/assets/0e16431f-eb2a-4f8a-a914-9bf92bf7c974)




