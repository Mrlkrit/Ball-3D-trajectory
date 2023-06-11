import cv2 as cv
import numpy as np
import glob
from natsort import natsorted


def calibrateCamera(img_path,pattern_size = (8,6)):

    # List of 3D points
    threed_points = []
    # List of 2D points
    twod_points = [] 

    # Defining the world coordinates for 3D points aka pattern coordinates
    objp = np.zeros((1, pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    objp = objp*0.12
    #print(objp)
    # Read path to calibration images
    images = glob.glob(img_path)
    images = natsorted(images)

    for fname in images:
        img = cv.imread(fname)
        img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv.findCirclesGrid(img_gray, pattern_size)

        if ret == True:
            threed_points.append(objp)
            twod_points.append(corners)

            # Draw detected points
            img = cv.drawChessboardCorners(img, pattern_size, corners, ret)
    
        #cv.imshow('img',img)
        #cv.waitKey(0)

    #cv.destroyAllWindows()


    ret, camera_matrix, distortion, rotation, translation = cv.calibrateCamera(threed_points, twod_points, img_gray.shape[::-1], None, None)


    return camera_matrix, distortion, rotation, translation
