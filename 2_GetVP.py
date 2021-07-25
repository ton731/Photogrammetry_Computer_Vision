import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt



img = cv.imread('road.png')
height = img.shape[0]
width = img.shape[1]

# use high-pass filter to sharpen the image
img_blur = cv.GaussianBlur(img, (0, 0), 100)
img_sharpen = cv.addWeighted(img, 1.5, img_blur, -0.5, 0)

gray = cv.cvtColor(img_sharpen, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150, apertureSize=3)




# get lines and erase the wrong lines
lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=400,maxLineGap=30)
a_matrix, b_matrix = [], []
for line in lines:
    x1,y1,x2,y2 = line[0]

    # remove near vertical and horizontal lines
    if(x1 == x2):continue
    slope = abs((y2-y1)/(x2-x1))
    if(slope>0.8):continue
    if(slope<0.2):continue
    if(y1<height/2 and y2<height/2):continue
    cv.line(img,(x1,y1),(x2,y2),(255,0,0),2)

    # calculate y=ax+b to find VP
    a = (y2-y1)/(x2-x1)
    b = y1 - a*x1
    a_matrix.append([a,-1])
    b_matrix.append(-1*b)




# use pseudo inverse to calculate vanishing point 
a_matrix = np.array(a_matrix)
b_matrix = np.array(b_matrix)
b_matrix = np.reshape(b_matrix, (1,-1))
x_y_matrix = np.matmul(np.linalg.pinv(a_matrix), b_matrix.T)
x, y = int(x_y_matrix[0][0]), int(x_y_matrix[1][0])
cv.circle(img, (x,y), radius=20, color=(255,0,0), thickness=5)
    




plt.imshow(img)
plt.show()

