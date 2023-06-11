import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from calibration import calibrateCamera
from detect_2D import getCoordinates
from calculate_3D_points import lineParams, calculate3DPoints, calculateMeanPoints
from filters import filterSinglePoints, filterDisplacementError
from fitting_curve import polynomialRegression3D





#path to data
calib_path_1= './sequence_3/camera_1/calib/*.jpg'
frames_path_1='./sequence_3/camera_1/frames/*.jpg'
calib_path_2= './sequence_3/camera_2/calib/*.jpg'
frames_path_2='./sequence_3/camera_2/frames/*.jpg'
calib_path_3= './sequence_3/camera_3/calib/*.jpg'
frames_path_3='./sequence_3/camera_3/frames/*.jpg'
# first and second sequence points for calibration
#points_3D_cam_1 = np.array([(9.0,9.0,0.0), (12.0,0.0,0.0), (12.0,9.0,0.0), (18.0,0.0,0.0), (18.0,9.0,0.0)])
#points_2D_cam_1 = np.array([(571,475), (96,842), (944,490), (1865,1026), (1841,526)],dtype=np.float64)

#points_3D_cam_2 = np.array([(9.0,0.0,0.0), (9.0,9.0,0.0), (12.0,0.0,0.0),(12.0,9.0,0.0), (18.0,0.0,0.0)])
#points_2D_cam_2 = np.array([(536,530), (1790,500), (473,620),(1976,581), (197,992)],dtype=np.float64)

#points_3D_cam_3 = np.array([(9.0,0.0,0.0),(9.0,9.0,0.0), (12.0,0.0,0.0), (12.0,9.0,0.0), (18.0,9.0,0.0)])
#points_2D_cam_3 = np.array([(209,536), (1468,545), (27,616), (1537,633),(1820,1000) ],dtype=np.float64)

# third sequence points for calibration
points_3D_cam_1 = np.array([(9.0,9.0,0.0), (12.0,0.0,0.0), (12.0,9.0,0.0), (9.0,0.0,0.0), (18.0,9.0,0.0)])
points_2D_cam_1 = np.array([(305,608), (1178,1066), (754,622), (174,1138), (1576,591)],dtype=np.float64)

points_3D_cam_2 = np.array([(9.0,9.0,0.0), (12.0,0.0,0.0), (12.0,9.0,0.0),(18.0,9.0,0.0), (18.0,0.0,0.0)])
points_2D_cam_2 = np.array([(572,474), (93,843), (945,490),(1841,524), (1863,1025)],dtype=np.float64)

points_3D_cam_3 = np.array([(9.0,0.0,0.0),(9.0,9.0,0.0), (12.0,0.0,0.0), (12.0,9.0,0.0), (18.0,0.0,0.0)])
points_2D_cam_3 = np.array([(535,529), (1791,500), (470,618), (1978,579),(195,990) ],dtype=np.float64)

if __name__ == "__main__":

    print("Calibration internal... ")
    camera_matrix_cam_1, distortion_cam_1, rotation_cam_1, translation_cam_1 = calibrateCamera(calib_path_1)
    camera_matrix_cam_2, distortion_cam_2, rotation_cam_2, translation_cam_2 = calibrateCamera(calib_path_2)
    camera_matrix_cam_3, distortion_cam_3, rotation_cam_3, translation_cam_3 = calibrateCamera(calib_path_3)

    print("Calibration external... ")
    ret,rot_1,trans_1 = cv.solvePnP(points_3D_cam_1,points_2D_cam_1,camera_matrix_cam_1,distortion_cam_1,cv.SOLVEPNP_ITERATIVE)
    ret,rot_2,trans_2 = cv.solvePnP(points_3D_cam_2,points_2D_cam_2,camera_matrix_cam_2,distortion_cam_2,cv.SOLVEPNP_ITERATIVE)
    ret,rot_3,trans_3 = cv.solvePnP(points_3D_cam_3,points_2D_cam_3,camera_matrix_cam_3,distortion_cam_3,cv.SOLVEPNP_ITERATIVE)

    rot_1, _ = cv.Rodrigues(rot_1)
    rot_2, _ = cv.Rodrigues(rot_2)
    rot_3, _ = cv.Rodrigues(rot_3)

    print("Calculating trajectory 1...")
    cam_1_trajectory_x,cam_1_trajectory_y = getCoordinates(frames_path_1)
    print("Calculating trajectory 2...")
    cam_2_trajectory_x,cam_2_trajectory_y = getCoordinates(frames_path_2)
    print("Calculating trajectory 3...")
    cam_3_trajectory_x,cam_3_trajectory_y = getCoordinates(frames_path_3)

    print("Calculating lines 1...")
    pos_vec_list_cam_1,dir_vec_list_cam_1 = lineParams(camera_matrix_cam_1,rot_1,trans_1,cam_1_trajectory_x,cam_1_trajectory_y)
    print("Calculating lines 2...")
    pos_vec_list_cam_2,dir_vec_list_cam_2= lineParams(camera_matrix_cam_2,rot_2,trans_2,cam_2_trajectory_x,cam_2_trajectory_y)
    print("Calculating lines 3...")
    pos_vec_list_cam_3,dir_vec_list_cam_3 = lineParams(camera_matrix_cam_3,rot_3,trans_3,cam_3_trajectory_x,cam_3_trajectory_y)


    print("Calculating 3D points 1_2...")
    points_3D_list_cam_1_2 = calculate3DPoints(pos_vec_list_cam_1,dir_vec_list_cam_1,pos_vec_list_cam_2,dir_vec_list_cam_2)
    print("Calculating 3D points 1_3...")
    points_3D_list_cam_1_3 = calculate3DPoints(pos_vec_list_cam_1,dir_vec_list_cam_1,pos_vec_list_cam_3,dir_vec_list_cam_3)
    print("Calculating 3D points 2_3...")
    points_3D_list_cam_2_3 = calculate3DPoints(pos_vec_list_cam_2,dir_vec_list_cam_2,pos_vec_list_cam_3,dir_vec_list_cam_3)

    print("Calculating mean points...")
    position_3D = calculateMeanPoints(points_3D_list_cam_1_2,points_3D_list_cam_1_3,points_3D_list_cam_2_3)

    print("Filtering 3D points...")
    position_3D = filterSinglePoints(position_3D)
    position_3D = filterDisplacementError(position_3D)

    print("Fitting curve...")
    position_3D = polynomialRegression3D(position_3D,20)

    #for i in range(0,540):
    #    print("frame: " + str(i))
    #    print("x: " + str(position_3D[i][0]) + " y: " + str(position_3D[i][1]) + " z: " + str(position_3D[i][2]))

    # display final trajectory
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []

    for i in position_3D:

        if not(i[0] == None):
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])

    ax.scatter(x, y, z, c='r', marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

    """
    Save to csv
    """
    position_3D_x = []
    position_3D_y = []
    position_3D_z = []

    for i in position_3D:
        position_3D_x.append(i[0])
        position_3D_y.append(i[1])
        position_3D_z.append(i[2])



    df = pd.DataFrame(data={"index": list(range(0,len(cam_1_trajectory_x))), "x1": cam_1_trajectory_x, "y1":cam_1_trajectory_y, "x2":cam_2_trajectory_x,
                               "y2": cam_2_trajectory_y, "x3":cam_3_trajectory_x,"y3":cam_3_trajectory_y,
                               "x": position_3D_x,"y": position_3D_y,"z": position_3D_z})
    df.to_csv("./file3.csv", sep=',',index=False)

    




