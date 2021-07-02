import numpy as np
import cv2
import time
import convolution_func


# 讀入照片
img = cv2.imread('Lebron.jpg', cv2.IMREAD_GRAYSCALE)


kernal = np.zeros(img.shape)
origin_x = img.shape[0]/2
origin_y = img.shape[1]/2
radius = 10
for i in range(len(kernal)):
    for j in range(len(kernal[0])):
        dis = (i-origin_x)**2 + (j-origin_y)**2
        if(dis <= radius**2):
            kernal[i][j] = 1
kernal = kernal / kernal.sum()



# 在頻率域相乘
def Frequency_Multiplication(img,mask):
    # 將相片轉換到頻率域
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # 將頻率的照片與filter相乘
    fshift_mask = fshift * mask

    # 將相乘後的結果，轉回空間域
    f_ishift = np.fft.ifftshift(fshift_mask)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.real(img_back)
    return img_back


rounds = 1000

start_1 = time.time()
for _ in range(rounds):
    convolution1 = cv2.filter2D(img,-1,kernal)
finish_1 = time.time()


start_3 = time.time()
for _ in range(rounds):
    convolution3 = Frequency_Multiplication(img,kernal)
finish_3 = time.time()



print('Total Round: ' + str(rounds))
print('cv2.filter2D time       : %8f' % (finish_1 - start_1))
# print('my convolution time     : %8f' % (finish_2 - start_2))
print('Frequence space multiply: %8f' % (finish_3 - start_3))
print('---------------------------------------------')