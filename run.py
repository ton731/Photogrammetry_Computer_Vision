import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import HelperFunction as h
import imutils

start = 1
finish = 1613
VP = np.zeros((2,finish-start+1))
last_direction_vector = [0, -1]
current_direction_vector = [0, 0]
angle_changed = np.zeros(finish-start+1)

x = 1

for i in range(start-1, finish):
    # print(i)

    # Initial set VP loc as last VP loc, if there is availble VP in this img,
    # then it will be replaced.
    if(x != 0):
        # VP[0][i], VP[1][i] = VP[0][i-1], VP[1][i-1]
        VP[0][i], VP[1][i] = 0, 0


    img = cv.imread(f'TonyRoadBig3Images/img{i+1}.jpg')
    # img = imutils.resize(img, width=800)
    height = img.shape[0]
    width = img.shape[1]
    direction_origin = [width/2, height]

    # use high-pass filter to sharpen the image
    img_blur = cv.GaussianBlur(img, (0, 0), 100)
    img_sharpen = cv.addWeighted(img, 1.5, img_blur, -0.5, 0)

    gray = cv.cvtColor(img_sharpen, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, threshold1=100, threshold2=150, apertureSize=3)


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

            cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
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
            cv.imwrite(f'TonyRoadBig3Images_VP/vp_img{i}.jpg', img)
            continue



        # use pseudo inverse to calculate vanishing point 
        a_matrix = np.array(a_matrix)
        b_matrix = np.array(b_matrix)
        b_matrix = np.reshape(b_matrix, (1,-1))
        x_y_matrix = np.matmul(np.linalg.pinv(a_matrix), b_matrix.T)
        x, y = int(x_y_matrix[0][0]), int(x_y_matrix[1][0])

        # If the VP is outsude the image, then skip this image
        if(x<0 or x>width or y<0 or y>height):continue

        # Update the vector, and calculate the angle changed
        # Assume turn right will get positive angle
        VP[0][i], VP[1][i] = x, y
        current_direction_vector = [VP[0][i] - direction_origin[0], VP[1][i] - direction_origin[1]]
        angle_changed[i] = h.GetAngleBetween2Vectors(last_vector=last_direction_vector, current_vector=current_direction_vector)
        last_direction_vector = current_direction_vector
        
        cv.circle(img, (x,y), radius=5, color=(0,0,255), thickness=2)
        cv.circle(img, (int(direction_origin[0]), int(direction_origin[1])),
                     radius=7, color=(0,255,255), thickness=10)
        cv.arrowedLine(img, (int(direction_origin[0]), int(direction_origin[1])),
                            (int(direction_origin[0]+current_direction_vector[0]*0.95), int(direction_origin[1]+current_direction_vector[1]*0.95)),
                            color=(0,255,255), thickness=3)


        print(f"img {i+1}: sussecced, get {good_line_count} good lines, showing image")
        cv.imwrite(f'TonyRoadBig3Images_VP/vp_img{i}.jpg', img)

        # plt.imshow(img)
        # plt.show()

    except Exception as e:
        print(f'error: img {i+1}, {e}')
        

f = open('TonyRoadBig3_Record.txt', 'w')
for i in range(finish-start+1):
    f.write(f"{i+1},{VP[0][i]},{VP[1][i]},{angle_changed[i]:.7f}\n")
f.close()

