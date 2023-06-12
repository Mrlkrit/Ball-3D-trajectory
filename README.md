Project done during studies, written in Python using OpenCV and numpy. It allows for 3D ball trajectory detection using images from 3 different cameras.
Stepps performed:
1. Internal and external camera calibration
2. 2D moving ball detection using Mixture of Gaussian, edge detection(Sobel algorithm) and region growth algorithm.
3. Calculate line parameters from camera center to the center of the ball
4. Calculating 3D points based on calculated lines crossing
5. Filtration of measurement errors and curve fitting to achieve smooth trajectory
6. Save tesults to csv file

For details please read CPO_Projekt file(written in Polish language).
