import numpy as np
import cv2


class Stitcher():
    def __init__(self):
        print('A Stich Job is Starting......')
    
    def stitch(self, images, ratio=0.75,  reprojThresh=4.0, showMatches=False):
        # detect keypoints, descriptors from images
        (img1, img2) = images
        (kp1, des1) = self.detectAndDescribe(img1)
        (kp2, des2) = self.detectAndDescribe(img2)

        # match keypoints between 2 images
        M = self.matchKeypoints(kp1, kp2, des1, des2, ratio, reprojThresh)

        # if the match is none, then there aren't enough matched keypoints to create a panorama
        if(M is None):
            return None

        # otherwise, apply a perspective warp to stitch the images together
        (matches, H, status) = M
        result = cv2.warpPerspective(img1, H, (img1.shape[1]+img2.shape[1], img1.shape[0]))
        result[0:img2.shape[0], 0:img2.shape[1]] = img2


        # check to see if the keypoint matches should be visualized
        if(showMatches):
            vis = self.drawMatches(img1, img2, kp1, kp2, matches, status)

            # return a tuple of the stiched image and the visualization
            return (result, vis)

        # only return the result stitched image
        return result


    def detectAndDescribe(self, img):
        print("Detecting and Describing......")
        # convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        surf = cv2.xfeatures2d.SURF_create(400)
        kp, des = surf.detectAndCompute(img, None)

        # convert the keypoints from Keypoint objects to numpy arrays
        kp = np.float32([k.pt for k in kp])

        # return a tuple of keypoint and descriptor
        return (kp, des)


    def matchKeypoints(self, kp1, kp2, des1, des2, ratio, reprojThresh):
        print("Matching Keypoints......")
        # compute the raw matches and initialize the list of actial matches
        # matcher = cv2.DescriptorMatcher_create("BruteForce")
        matcher = cv2.BFMatcher()
        rawMatches = matcher.knnMatch(des1, des2, k=2)
        matches = []

        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each other
            if(len(m) == 2 and m[0].distance < m[1].distance * ratio):
                matches.append((m[0].trainIdx, m[0].queryIdx))
        
        # computing a homography requires at least 4 matches
        if(len(matches) > 4):
            # construct the two sets of points
            pts1 = np.float32([kp1[i] for (_,i) in matches])
            pts2 = np.float32([kp2[i] for (i,_) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(pts1, pts2, cv2.RANSAC, reprojThresh)

            # return thematches aling with the homography matrix and status of each matched point
            return (matches, H, status)

        # otherwise, no homography could be computed
        return None


    def drawMatches(self, img1, img2, kp1, kp2, matches, status):
        print("Drawing Matches......")
        # initialize the output visualization image
        (h1, w1) = img1.shape[:2]
        (h2, w2) = img2.shape[:2]
        vis = np.zeros((max(h1,h2), w1+w2, 3), dtype="uint8")
        vis[0:h1, 0:w1] = img1
        vis[0:h2, w1:] = img2

        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully matched
            if(s == 1):
                # draw the match
                pt1 = (int(kp1[queryIdx][0]), int(kp1[queryIdx][1]))
                pt2 = (int(kp2[trainIdx][0])+w1, int(kp2[trainIdx][1]))
                cv2.line(vis, pt1, pt2, (0,255,0),1)
        
        # return the visualization
        return vis


