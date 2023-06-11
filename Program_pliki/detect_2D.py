import cv2 as cv
import numpy as np
import glob 
from natsort import natsorted

"""
Detect center of ball and return x,y trajectory
"""
def getCoordinates(path_to_frames,remove_size_MoG=1000,remove_size_Sobel=120):

    background_subtraction = cv.createBackgroundSubtractorMOG2()
    background_subtraction.setHistory(5)
    background_subtraction.setDetectShadows(False)

    images_paths = glob.glob(path_to_frames)
    images_paths = natsorted(images_paths)

    # model
    for frame in images_paths[0:5:1]:

        img = cv.imread(frame,-1)

        mask = background_subtraction.apply(img)
        mask = cv.dilate(mask,None)
        mask = cv.GaussianBlur(mask, (15, 15),0)     
        ret,mask = cv.threshold(mask,0,255,cv.THRESH_BINARY | cv.THRESH_OTSU)

    # main loop
    prev_sobel = None
    trajectory_x = []
    trajectory_y = []

    for frame in images_paths:

        #Read frame
        img = cv.imread(frame,-1)

        #Mixture of gaussian
        mask = background_subtraction.apply(img)  
        mask = cv.dilate(mask,None)
        mask = cv.GaussianBlur(mask, (15, 15),0)
        ret,mask = cv.threshold(mask,0,255,cv.THRESH_BINARY | cv.THRESH_OTSU)

        #cv.imshow("maskMoG", mask)
        #Grayscale
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray,(15,15),0)
    
        #Sobel
        image_sobel = cv.Sobel(gray,ddepth=cv.CV_8U,dx=1,dy=1,ksize=3)
        

        #Delete small blobs from MoG
        blob_amount, out, stats, centroids = cv.connectedComponentsWithStats(mask, 8)
        sizes = stats[1:, -1]; 
        blob_amount = blob_amount - 1
        image = np.zeros((out.shape))
        for i in range(0, blob_amount):
            if sizes[i] >= remove_size_MoG:
                image[out == i + 1] = 255

        #cv.imshow("MoG", image)



        #Subtract previous sobel - current sobel, filter out small objects
        image_sobel_filtered = np.zeros((out.shape))
        if prev_sobel is not None:
            subtract_sobel = prev_sobel - image_sobel
            subtract_sobel = cv.erode(subtract_sobel,(5,5),iterations=4)
            #cv.imshow("sobel1", subtract_sobel)
            blob_amount, out, stats, centroids = cv.connectedComponentsWithStats(subtract_sobel, 8)
            sizes = stats[1:, -1]; 
            blob_amount = blob_amount - 1

            for i in range(0, blob_amount):
                if sizes[i] >= remove_size_Sobel:
                    image_sobel_filtered[out == i + 1] = 255

        #cv.imshow("Sobel_Filtered",image_sobel_filtered)

        prev_sobel=image_sobel

        #Draw contours and find coordinates
        image_norm = cv.normalize(image, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
        cnts = cv.findContours(image_norm, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        pixel_count = 0
        prev_amount = 0
        coord_x = -1
        coord_y = -1
    
        image_sobel_filtered = cv.normalize(image_sobel_filtered, dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)

        for c in cnts:

            x,y,w,h = cv.boundingRect(c)
            cv.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 3)

            # check the window in sobel image for white pixels
            for rows in range(x,x+w):
                for cols in range(y,y+h):

                    if image_sobel_filtered[cols,rows] == 255:
                        pixel_count = pixel_count + 1

            #take object with the highest number of white pixels in sobel
            if pixel_count > prev_amount:
                coord_x = float(x + w/2)
                coord_y = float(y + h/2)
                prev_amount = pixel_count

        trajectory_x.append(coord_x)
        trajectory_y.append(coord_y)

        #cv.imshow("Processed",image)
        #cv.imshow("Ball",img)
        #cv.waitKey(0)
    return trajectory_x, trajectory_y
    


    











    #cv.waitKey(0)




#cv.waitKey(0)
#print(trajectory)


