import numpy as np
import cv2
import convolution_func
import time

img = cv2.imread('Lebron.jpg', cv2.IMREAD_GRAYSCALE)

# img = np.zeros((5,5))
# count = 1
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         img[i][j] = count
#         count += 1

# kernal = np.array([[0,1,0],[1,0,1],[0,1,0]])
kernal = np.array((
        [0.0625, 0.125, 0.0625],
        [0.125, 0.25, 0.125],
        [0.0625, 0.125, 0.0625]))

# convolution1 = cv2.filter2D(img,-1,kernal)
# convolution2 = convolution_func.my_convolution(img, kernal)

rounds = 1000

start_1 = time.time()
for _ in range(rounds):
    convolution1 = cv2.filter2D(img,-1,kernal)
finish_1 = time.time()

start_2 = time.time()
for _ in range(rounds):
    convolution2 = convolution_func.my_convolution(img,kernal)
finish_2 = time.time()

print('Total Round: ' + str(rounds))
print('cv2.filter2D time  : %8f' % (finish_1 - start_1))
print('my convolution time: %8f' % (finish_2 - start_2))
print('---------------------------------------------')


# print(convolution1)
# print('-----------------------')
# print(convolution2)