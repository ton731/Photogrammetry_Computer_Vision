import cv2 as cv


vidcap = cv.VideoCapture('Video/TonyRoadBig3.mp4')
success,image = vidcap.read()
count = 1

while success:
    if(count%5 == 0):
        index = int(count/5)
        cv.imwrite(f"TonyRoadBig3Images/img{index}.jpg", image)     # save frame as JPEG file      
        print('Read a new frame: ', index)
    success,image = vidcap.read()
    count += 1