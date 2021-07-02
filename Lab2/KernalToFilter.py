import numpy as np
import cv2
import matplotlib.pyplot as plt


# 將img從空間域轉換到頻率域
img = cv2.imread('dog.jpg', cv2.IMREAD_GRAYSCALE)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)


# 在空間域做kernal
kernel = np.zeros((100,100))
for i in range(100):
    for j in range(100):
        kernel[i][j] = (50 - abs(50-i)) * (50 - abs(50-j))
kernel = kernel / kernel.sum()


# 在空間域先resize
kernel_resize = np.zeros(img.shape)
for i in range(100):
    for j in range(100):
        i_index = int((img.shape[0])/2) - 50 + i
        j_index = int((img.shape[1])/2) - 50 + j
        kernel_resize[i_index][j_index] = kernel[i][j]






# 將kernal轉到頻率域
kernel_f = np.fft.fft2(kernel_resize)
kernel_f = np.fft.fftshift(kernel_f)
kernel_f = np.real(kernel_f)

# kernel_f_resize = np.zeros(img.shape)
# for i in range(len(kernel_f_resize)):
#     for j in range(len(kernel_f_resize[0])):
#         i_index = int(i / (1244/100))
#         j_index = int(j / (1983/100))
#         kernel_f_resize[i][j] = kernel_f[i_index][j_index]
# kernel_f_resize = kernel_f_resize / kernel_f_resize.sum()


# kernel_f_resize = np.zeros(img.shape)
# for i in range(100):
#     for j in range(100):
#         i_index = int((img.shape[0])/2) - 50 + i
#         j_index = int((img.shape[1])/2) - 50 + j
#         kernel_f_resize[i_index][j_index] = kernel_f[i][j]




img_convolution = cv2.filter2D(img,-1,kernel)
     


# 在頻率域中相乘
img = cv2.imread('dog.jpg', cv2.IMREAD_GRAYSCALE)
img_f = np.fft.fft2(img)
img_f = np.fft.fftshift(img_f)

img_kernel_f = img_f * kernel_f

# 將照片轉回空間域
img_s = np.fft.ifftshift(img_kernel_f)
img_s = np.fft.ifft2(img_s)
img_s = np.fft.ifftshift(img_s)
img_s = np.real(img_s)



# plt.subplot(231)
# plt.imshow(img, cmap = 'gray')
# plt.title('input image')

plt.subplot(231)
plt.imshow(kernel, cmap = 'gray')
plt.title('kernel (spatial space)')

plt.subplot(232)
plt.imshow(kernel_resize, cmap = 'gray')
plt.title('kernel resize (spatial space)')

plt.subplot(233)
plt.imshow(kernel_f, cmap = 'gray')
plt.title('kernel (frequence space)')



plt.subplot(234)
plt.imshow(img_convolution, cmap = 'gray')
plt.title('spatial space convolution')

plt.subplot(235)
plt.imshow(img_s, cmap = 'gray')
plt.title('frequence space multiplication')

plt.show()

