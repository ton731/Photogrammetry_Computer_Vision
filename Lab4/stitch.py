from panorama import Stitcher
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True, help="path to the first image")
ap.add_argument("-s", "--second", required=True, help="path to the second image")
args = vars(ap.parse_args())


# load the two images and resize them to have a width of 400 pixels for faster processing
img1 = cv2.imread(args["first"])
img2 = cv2.imread(args["second"])
img1 = imutils.resize(img1, width=800)
img2 = imutils.resize(img2, width=800)

# stitch the image together to create a panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([img1, img2], showMatches=True)

# show the image
# cv2.imshow("Image 1", img1)
# cv2.imshow("Image 2", img2)
# cv2.imshow("keypoints Matches", vis)
# cv2.imshow("Result", result)
# cv2.waitKey(0)
cv2.imwrite('result.jpg', result)