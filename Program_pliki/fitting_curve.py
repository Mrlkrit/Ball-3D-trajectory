import numpy as np
#import matplotlib.pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
"""
Fit polynomial curve to 3D points
"""
def polynomialRegression3D(points_3D, degree):

    x = []
    y = []
    z = []

    for i in points_3D:
        if not(i[0] == None):
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    
    data_yz = np.array([y,z])
    data_yz = data_yz.transpose()

    polynomial_features = PolynomialFeatures(degree=degree)
    x_poly = polynomial_features.fit_transform(x[:, np.newaxis])


    model = LinearRegression()
    model.fit(x_poly, data_yz)
    y_poly_pred = model.predict(x_poly)


    # display
    #fig = plt.figure()
    #ax = plt.axes(projection='3d')
    #ax.scatter(x, data_yz[:,0], data_yz[:,1])
    #ax.plot(x, y_poly_pred[:,0], y_poly_pred[:,1], color='r')
    #ax.set_xlabel('X')
    #ax.set_ylabel('Y')
    #ax.set_zlabel('Z')


    fit_3D_points = []
    iterator = 0
    for i in range(0,len(points_3D)):
        if not(points_3D[i][0] == None):
            fit_3D_points.append([x[iterator],y_poly_pred[iterator][0],y_poly_pred[iterator][1]])
            iterator = iterator + 1
        else:
            fit_3D_points.append([None,None,None])



    #plt.show()

    return fit_3D_points