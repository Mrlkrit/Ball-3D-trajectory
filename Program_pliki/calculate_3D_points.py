import numpy as np

"""
Calculate line parameters
"""
def lineParams(camera_matrix,rotation,translation,trajectory_x,trajectory_y):

    fx = camera_matrix[0,0]
    fy = camera_matrix[1,1]
    cx = camera_matrix[0,2]
    cy = camera_matrix[1,2]

    dir_vec_list = []
    dummy = np.array([None])

    rot_inv = rotation.T
    pos_vec = -(np.dot(rot_inv,translation))

    for i in range(0,len(trajectory_x)):
        # append dummy if no point
        if  trajectory_x[i] == -1:

            dir_vec_list.append(dummy)
        # calculate line
        else:

            x_norm = (trajectory_x[i] - cx)/fx
            y_norm = (trajectory_y[i] - cy)/fy

            p_norm = np.array([x_norm,y_norm,1])

            dir_vec = np.dot(rot_inv,p_norm)
            dir_vec_list.append(dir_vec)
            
    return pos_vec,np.array(dir_vec_list)

"""
Calculate 3D point based on line crossing
"""
def calculate3DPoints(pos_vec_list_1,dir_vec_list_1,pos_vec_list_2,dir_vec_list_2):

    point_3D_list = []
    dummy = np.array([None])

    A = pos_vec_list_1
    B = pos_vec_list_2
    c = B-A


    for i in range(0,len(dir_vec_list_2)):
        # if no points append None
        if len(dir_vec_list_1[i]) == 1 or len(dir_vec_list_2[i]) == 1:

            point_3D_list.append(dummy)
        # point calculation
        else:

            a = dir_vec_list_1[i]
            b = dir_vec_list_2[i]

            ab = np.dot(a,b)
            ac = np.dot(a,c)
            bc = np.dot(b,c)
            aa = np.dot(a,a)
            bb = np.dot(b,b)

            A_resh = np.reshape(A,(1,3))
            B_resh = np.reshape(B,(1,3))
            
            D = A_resh + a*(ac*bb-ab*bc)/(aa*bb-ab*ab)
            E = B_resh + a*(ab*ac-bc*aa)/(aa*bb-ab*ab)

            point_3D = 0.5*(D+E)
            point_3D = point_3D.tolist()

            point_3D_list.append(point_3D[0])

    return point_3D_list
'''
Calculate mean value based on number of points
'''
def calculateMeanPoints(points_1,points_2,points_3):

    mean_3D_points = []

    for i in range(0,len(points_1)):
        # no points
        if len(points_1[i])==1 and  len(points_2[i])==1 and  len(points_3[i])==1:

            mean_3D_points.append([None,None,None])
        # only point 3
        elif len(points_1[i])==1 and len(points_2[i])==1:

            mean_3D_points.append(points_3[i])
        # only point 2
        elif len(points_1[i])==1 and len(points_3[i])==1:

            mean_3D_points.append(points_2[i])
        # only point 1
        elif len(points_2[i])==1 and len(points_3[i])==1:

            mean_3D_points.append(points_1[i])
        # points 2 and 3
        elif len(points_1[i]) == 1:

            x1 = points_2[i][0]
            y1 = points_2[i][1]
            z1 = points_2[i][2]
            x2 = points_3[i][0]
            y2 = points_3[i][1]
            z2 = points_3[i][2]

            mean_3D_points.append([(x1+x2)/2, (y1+y2)/2, (z1+z2)/2])
        # points 1 and 3
        elif len(points_2[i]) == 1:

            x1 = points_1[i][0]
            y1 = points_1[i][1]
            z1 = points_1[i][2]
            x2 = points_3[i][0]
            y2 = points_3[i][1]
            z2 = points_3[i][2]

            mean_3D_points.append([(x1+x2)/2.0, (y1+y2)/2.0, (z1+z2)/2.0])
        # points 1 and 2
        elif len(points_3[i]) == 1:

            x1 = points_2[i][0]
            y1 = points_2[i][1]
            z1 = points_2[i][2]
            x2 = points_1[i][0]
            y2 = points_1[i][1]
            z2 = points_1[i][2]

            mean_3D_points.append([(x1+x2)/2.0, (y1+y2)/2.0, (z1+z2)/2.0])
        # all 3 points
        else:

            x1 = points_1[i][0]
            y1 = points_1[i][1]
            z1 = points_1[i][2]
            x2 = points_2[i][0]
            y2 = points_2[i][1]
            z2 = points_2[i][2]
            x3 = points_3[i][0]
            y3 = points_3[i][1]
            z3 = points_3[i][2]

            mean_3D_points.append([(x1+x2+x3)/3.0, (y1+y2+y3)/3.0, (z1+z2+z3)/3.0])

    return mean_3D_points