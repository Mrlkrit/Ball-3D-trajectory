
"""
Filtering single points that are pretty far from neighbours
"""
def filterSinglePoints(position_3D):

    for i in range(1,len(position_3D)-2):

        if not(position_3D[i][0]==None) and not(position_3D[i+1][0]==None) and not(position_3D[i-1][0]==None) and not(position_3D[i+2][0]==None):

            if abs(position_3D[i][1]-position_3D[i-1][1])>0.5 and not(abs(position_3D[i+2][1]-position_3D[i-1][1])>0.5):
                position_3D[i][1] = (position_3D[i-1][1] + position_3D[i+1][1])/2
    return position_3D

"""
Filter the points in a way that they are supposed to be continuous 
"""
def filterDisplacementError(position_3D):

    grad_x_current = [0]
    grad_y_current = [0]
    grad_z_current = [0]
    subtract_val_x = 0
    subtract_val_y = 0
    subtract_val_z = 0

    last_3D_point_index = None
    """
    Here we try to find the moment when points are not continuous
    it will have large gradient there
    """
    for i in range(1,len(position_3D)):

        if position_3D[i-1][0]==None:

            grad_x_current.append(0)
            grad_y_current.append(0)
            grad_z_current.append(0)

        elif not(position_3D[i][0]==None):

            grad_x_current.append(position_3D[i][0]-position_3D[i-1][0])
            grad_y_current.append(position_3D[i][1]-position_3D[i-1][1])
            grad_z_current.append(position_3D[i][2]-position_3D[i-1][2])
            last_3D_point_index = i
        else:

            grad_x_current.append(0)
            grad_y_current.append(0)
            grad_z_current.append(0)

    """
    Move the points if gradient is larger than specified
    """
    for i in range(1,len(position_3D)):

        if not(position_3D[i][0]==None) and not(position_3D[i+1][0]==None) and not(position_3D[i-1][0]==None):

                if abs(grad_x_current[i])>=0.4:
                    subtract_val_x = subtract_val_x + grad_x_current[i]
        
                if abs(grad_y_current[i])>=0.4:
                    subtract_val_y = subtract_val_y + grad_y_current[i]
        
                if abs(grad_z_current[i])>=0.4:
                    subtract_val_z = subtract_val_z + grad_z_current[i]

                position_3D[i][0] = position_3D[i][0] - subtract_val_x
                position_3D[i][1] = position_3D[i][1] - subtract_val_y
                position_3D[i][2] = position_3D[i][2] - subtract_val_z
    """
    Move last element
    """
    if last_3D_point_index is not None:
        position_3D[last_3D_point_index][0] = position_3D[last_3D_point_index][0] - subtract_val_x
        position_3D[last_3D_point_index][1] = position_3D[last_3D_point_index][1] - subtract_val_y
        position_3D[last_3D_point_index][2] = position_3D[last_3D_point_index][2] - subtract_val_z

    return position_3D