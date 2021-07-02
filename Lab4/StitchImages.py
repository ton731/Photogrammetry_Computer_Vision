import numpy as np
import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('img1.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('img2.jpg', cv2.IMREAD_GRAYSCALE)


# -------------------------------------------------------------


# Feature Detection
surf = cv2.xfeatures2d.SURF_create(5000)

# find the keypoints and descriptors with SIFT
kp1, des1 = surf.detectAndCompute(img1,None)
kp2, des2 = surf.detectAndCompute(img2,None)


# -------------------------------------------------------------


# Feature Matching
# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)
matches_1 = [m for m,n in matches]

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])


# cv.drawMatchesKnn expects list of lists as matches.
# img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,matchColor=(0,255,0),
#                         singlePointColor=(0,0,255),flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches_1,None,matchColor=(0,255,0),
#                         singlePointColor=(0,0,255),flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
# plt.imshow(img3)
# plt.show()


# -------------------------------------------------------------


# Homogrophy Estimation











