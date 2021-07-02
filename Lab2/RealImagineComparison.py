import numpy as np
import cv2
import matplotlib.pyplot as plt


# 將img從空間域轉換到頻率域
img = cv2.imread('Lebron.jpg', cv2.IMREAD_GRAYSCALE)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)


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


# 將相乘後的結果，轉回空間域
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_real = np.real(img_back)
img_imag = np.imag(img_back)




plt.subplot(131)
plt.imshow(img, cmap = 'gray')
plt.title('Input Image')
plt.subplot(132)
plt.imshow(img_real, cmap = 'gray')
plt.title('Inverse Image (Real Part)')
plt.subplot(133)
plt.imshow(img_imag, cmap = 'gray')
plt.title('Inverse Image (Imag Part)')
# plt.imshow(img - img_real, cmap = 'gray')
# plt.title('Input Img - Inverse Img (Real part)')

plt.show()