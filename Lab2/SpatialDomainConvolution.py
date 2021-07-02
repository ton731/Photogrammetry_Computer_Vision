import numpy as np
import cv2
import matplotlib.pyplot as plt
import convolution_func

# 讀入照片
img = cv2.imread('dog.jpg', cv2.IMREAD_GRAYSCALE)

# 製作filter
# filterr = np.array((
#         [0.25, 0.0, 0.25],
#         [0.0, 0.0, 0.0],
#         [0.25, 0.0, 0.25]))    
# filterr = filterr / filterr.sum()

filterr = np.zeros(img.shape)
origin_x = img.shape[0]/2
origin_y = img.shape[1]/2
radius = 30
for i in range(len(filterr)):
    for j in range(len(filterr[0])):
        dis = (i-origin_x)**2 + (j-origin_y)**2
        if(dis <= radius**2):
            filterr[i][j] = 1
# filterr = filterr / filterr.sum()
# filterr = filterr / filterr.max()
filterr = filterr * 2 - 1


# 將filter轉回spatial space
filter_spatial = np.fft.ifftshift(filterr)
filter_spatial = np.fft.ifft2(filter_spatial)



filter_spatial_real = np.real(filter_spatial)
filter_spatial_imag = np.imag(filter_spatial)
filter_spatial_real = filter_spatial_real / filter_spatial_real.sum()
filter_spatial_imag = filter_spatial_imag / filter_spatial_imag.sum()

# print(filter_spatial)


convolution_frequence = cv2.filter2D(img,-1,filterr)
convolution_spatial_real = cv2.filter2D(img,-1,filter_spatial_real)
convolution_spatial_imag = cv2.filter2D(img,-1,filter_spatial_imag)


# plt.subplot(131)
# plt.imshow(img, cmap = 'gray')
# plt.title('Original')

plt.subplot(131)
plt.imshow(filterr, cmap = 'gray')
plt.title('filter (frequence)')

plt.subplot(132)
plt.imshow(np.real(filter_spatial), cmap = 'gray')
plt.title('filter (frequence to spatial real)')

# plt.subplot(244)
# plt.imshow(np.imag(filter_spatial), cmap = 'gray')
# plt.title('filter (frequence to spatial imag)')

# plt.subplot(132)
# plt.imshow(convolution_frequence, cmap = 'gray')
# plt.title('cv2.Filter2D (frequence filter)')

plt.subplot(133)
plt.imshow(convolution_spatial_real, cmap = 'gray')
plt.title('cv2.Filter2D (spatial filter real)')

# plt.subplot(224)
# plt.imshow(convolution_spatial_imag, cmap = 'gray')
# plt.title('cv2.Filter2D (spatial filter imag)')

plt.show()


# cv2.imwrite('filter_spatial.jpg',np.real(filter_spatial))
# print(np.real(filter_spatial).max())