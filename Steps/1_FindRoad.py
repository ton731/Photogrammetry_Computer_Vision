import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import imutils

img = cv.imread('road.png')
height = img.shape[0]
width = img.shape[1]

img_blur = cv.GaussianBlur(img, (0, 0), 100)
img_blur = cv.GaussianBlur(img_blur, (0, 0), 100)
img_blur = cv.GaussianBlur(img_blur, (0, 0), 100)

img_sharpen = cv.addWeighted(img, 1.5, img_blur, -0.5, 0)

gray = cv.cvtColor(img_sharpen, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150, apertureSize=3)





lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=400,maxLineGap=30)
for line in lines:
    x1,y1,x2,y2 = line[0]


    # Remove near vertical and horizontal lines
    if(x1 == x2):continue

    slope = abs((y2-y1)/(x2-x1))

    if(slope>0.8):continue
    if(slope<0.2):continue
    if(y1<height/2 and y2<height/2):continue
    
    cv.line(img,(x1,y1),(x2,y2),(255,0,0),2)




plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.imshow(img_sharpen)

# plt.imshow(img)
plt.show()

