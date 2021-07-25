import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import HelperFunction as h
import imutils

start = 1
finish = 421
x = 8

for i in range(x, x+1):
    # print(i)

    img = cv.imread(f'Images/img{i}.jpg')
    img = imutils.resize(img, width=800)
    height = img.shape[0]
    width = img.shape[1]

    # use high-pass filter to sharpen the image
    img_blur = cv.GaussianBlur(img, (0, 0), 100)
    img_sharpen = cv.addWeighted(img, 1.5, img_blur, -0.5, 0)

    gray = cv.cvtColor(img_sharpen, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, threshold1=100, threshold2=150, apertureSize=3)


    # plt.imshow(edges)
    # plt.show()
# 


    try:
        # get lines and erase the wrong lines
        lines = cv.HoughLinesP(edges,rho=1,theta=np.pi/180,threshold=100,minLineLength=100,maxLineGap=25)
        a_matrix, b_matrix = [], []
        good_line_count = 0
        has_left_line = False
        has_right_line = False
        for line in lines:
            x1,y1,x2,y2 = line[0]
            
            if(h.CheckIfGoodLine(x1,y1,x2,y2,height,width) == False):
                continue

            cv.line(img,(x1,y1),(x2,y2),(0,0,255),1)
            good_line_count += 1
            if((y2-y1)/(x2-x1)<0): has_left_line = True
            if((y2-y1)/(x2-x1)>0): has_right_line = True

            # calculate y=ax+b to find VP
            a = (y2-y1)/(x2-x1)
            b = y1 - a*x1
            a_matrix.append([a,-1])
            b_matrix.append(-1*b)

        # If good lines are less than 2, if means the image is not good enough, skip to next
        if(good_line_count < 2 or has_left_line == False or has_right_line == False):
            print(f"{i}: only {good_line_count} good lines, left line: {has_left_line}, right line: {has_right_line}")
            continue



        # use pseudo inverse to calculate vanishing point 
        a_matrix = np.array(a_matrix)
        b_matrix = np.array(b_matrix)
        b_matrix = np.reshape(b_matrix, (1,-1))
        x_y_matrix = np.matmul(np.linalg.pinv(a_matrix), b_matrix.T)
        x, y = int(x_y_matrix[0][0]), int(x_y_matrix[1][0])
        cv.circle(img, (x,y), radius=7, color=(0,0,255), thickness=4)


        print(f"{i}: sussecced, get {good_line_count} good lines, showing image")
        # cv.imwrite(f'Images_VP_resize_800/vp_img{i}.jpg', img)
        # cv.imwrite("VP.jpg", img)

        plt.imshow(img)
        plt.show()

    except Exception as e:
        print(f'error: {i}, {e}')
        

