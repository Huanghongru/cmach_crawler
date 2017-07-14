import os
import cv2
import numpy as np

img = cv2.imread('test.jpg')
subimg = img[1400:1800, 1400:1800]

cv2.namedWindow('image')
cv2.imshow('image', subimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
