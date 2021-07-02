import numpy as np

def my_convolution(image, kernal):
  m, n = image.shape[0], image.shape[1]
  a, b = kernal.shape[0], kernal.shape[1]
  h, w = m-a+1, n-b+1
  new = np.zeros((h,w))

  # for every point in the conv matrix
  for i in range(h):
    for j in range(w):
      # calculate the aggregated multiplication value in the kernel
      new[i, j] = np.multiply(image[i:i+a, j:j+b], kernal).sum()
      
  return new