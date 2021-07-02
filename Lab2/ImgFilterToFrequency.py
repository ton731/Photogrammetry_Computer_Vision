import numpy as np
import cv2
import matplotlib.pyplot as plt


# 將img從空間域轉換到頻率域
img = cv2.imread('dog.jpg', cv2.IMREAD_GRAYSCALE)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))


# 直接在頻率域做low-pass filter
mask = np.zeros(img.shape)
origin_x = img.shape[0]/2
origin_y = img.shape[1]/2
radius = 30
for i in range(len(mask)):
    for j in range(len(mask[0])):
        dis = (i-origin_x)**2 + (j-origin_y)**2
        if(dis <= radius**2):
            mask[i][j] = 1
mask = mask / mask.sum()

# 將頻率的照片與filter相乘
fshift_mask = fshift * mask


# 將相乘後的結果，轉回空間域
f_ishift = np.fft.ifftshift(fshift_mask)
img_back = np.fft.ifft2(f_ishift)
img_back = np.real(img_back)

# print(img_back)

plt.subplot(231)
plt.imshow(img, cmap = 'gray')
plt.title('Input Image')
plt.subplot(232)
plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Image frequency')
plt.subplot(233)
plt.imshow(mask, cmap = 'gray')
plt.title('Filter frequency')
plt.subplot(234)
plt.imshow(magnitude_spectrum*mask, cmap = 'gray')
plt.title('Img f * Filter f')
plt.subplot(235)
plt.imshow(img_back, cmap = 'gray')
plt.title('Img fft inverse')

plt.show()